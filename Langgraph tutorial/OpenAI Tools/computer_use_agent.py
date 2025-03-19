#!/usr/bin/env python3
import time
import base64
import datetime
from openai import OpenAI 
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def log_action(task_log, message):
    """Log an action with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    task_log.append(entry)

def handle_model_action(page, action, task_log):
    """
    Execute a computer action (click, scroll, keypress, type, wait) on the Playwright page.
    Log a brief summary of the executed action into task_log.
    """
    try:
        action_type = action.type  
        summary = ""
        if action_type == "click":
            x, y = action.x, action.y
            button = action.button if action.button in ["left", "right"] else "left"
            summary = f"Clicked at ({x}, {y}) with {button} button."
            page.mouse.click(x, y, button=button)
        elif action_type == "scroll":
            x, y = action.x, action.y
            scroll_x = getattr(action, "scroll_x", 0)
            scroll_y = getattr(action, "scroll_y", 0)
            summary = f"Scrolled at ({x}, {y}) with offsets (scroll_x={scroll_x}, scroll_y={scroll_y})."
            page.mouse.move(x, y)
            page.evaluate(f"window.scrollBy({scroll_x}, {scroll_y})")
        elif action_type == "keypress":
            keys = action.keys
            summary = f"Pressed keys: {' '.join(keys)}."
            for k in keys:
                if k.lower() == "enter":
                    page.keyboard.press("Enter")
                elif k.lower() == "space":
                    page.keyboard.press(" ")
                else:
                    page.keyboard.press(k)
        elif action_type == "type":
            text = action.text
            summary = f"Typed text: {text}."
            page.keyboard.type(text)
        elif action_type == "wait":
            summary = "Waited for 1 second."
            time.sleep(1)  # Short wait
        elif action_type == "screenshot":
            summary = "Screenshot action (no direct input)."
        else:
            summary = f"Unrecognized action: {action}."
        log_action(task_log, summary)
    except Exception as e:
        err_msg = f"Error handling action {action}: {e}"
        log_action(task_log, err_msg)

def get_screenshot(page, task_log):
    """
    Wait for the page to stabilize and then capture a viewport screenshot.
    Uses a re-try loop to handle timeouts. The screenshot is captured as a JPEG
    with reduced quality to speed up processing.
    """
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception as e:
        log_action(task_log, f"Warning: wait_for_load_state encountered an error: {e}")
    page.wait_for_timeout(500)  # Shorter wait to avoid long delays

    # Attempt to take a screenshot up to 3 times.
    for attempt in range(1, 4):
        try:
            log_action(task_log, f"Taking screenshot (attempt {attempt})...")
            # Lower quality and full_page=False to keep the image small.
            screenshot = page.screenshot(timeout=60000, type="jpeg", quality=30, full_page=False)
            log_action(task_log, "Screenshot captured successfully.")
            return screenshot
        except PlaywrightTimeoutError as e:
            log_action(task_log, f"Screenshot attempt {attempt} timed out: {e}")
            time.sleep(1)  # Wait a bit before retrying
    raise Exception("Failed to capture screenshot after multiple attempts.")

def extract_reasoning_summary(response, task_log):
    """
    Extract any reasoning summary provided by the final response and log it.
    """
    reasoning_items = [item for item in response.output if getattr(item, "type", None) == "reasoning"]
    if reasoning_items:
        for item in reasoning_items:
            summaries = getattr(item, "summary", [])
            for s in summaries:
                summary_text = getattr(s, "text", "")
                log_action(task_log, f"Final reasoning summary: {summary_text}")
    else:
        log_action(task_log, "No final reasoning summary provided.")

def computer_use_loop(page, client, response):
    """
    Execute computer actions until no more 'computer_call' items are returned.
    Capture screenshots, send them to the model, and log each step.
    """
    task_log = []
    log_action(task_log, "Starting task execution loop.")
    
    while True:
        computer_calls = [item for item in response.output if getattr(item, "type", None) == "computer_call"]
        if not computer_calls:
            log_action(task_log, "No computer call found in the model response.")
            for item in response.output:
                log_action(task_log, f"Final output item: {item}")
            break
        
        computer_call = computer_calls[0]
        last_call_id = computer_call.call_id
        action = computer_call.action
        
        # Process pending safety checks.
        acknowledged_safety_checks = []
        if hasattr(computer_call, "pending_safety_checks") and computer_call.pending_safety_checks:
            for safety in computer_call.pending_safety_checks:
                log_action(task_log, f"Pending safety check: {safety.message}")
                acknowledged_safety_checks.append(safety)
        
        handle_model_action(page, action, task_log)
        time.sleep(0.5)
        
        try:
            screenshot_bytes = get_screenshot(page, task_log)
        except Exception as e:
            log_action(task_log, f"Error capturing screenshot: {e}")
            break  # Break the loop if screenshot fails.
            
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
        
        input_item = {
            "call_id": last_call_id,
            "type": "computer_call_output",
            "output": {
                "type": "computer_screenshot",
                "image_url": f"data:image/jpeg;base64,{screenshot_base64}"
            }
        }
        if acknowledged_safety_checks:
            input_item["acknowledged_safety_checks"] = acknowledged_safety_checks
        
        log_action(task_log, "Sending updated screenshot to model.")
        response = client.responses.create(
            model="computer-use-preview",
            previous_response_id=response.id,
            tools=[{
                "type": "computer_use_preview",
                "display_width": 1024,
                "display_height": 768,
                "environment": "linux"
            }],
            input=[input_item],
            truncation="auto"
        )
    
    log_action(task_log, "=== Task Completed ===")
    extract_reasoning_summary(response, task_log)
    
    print("\n=== Task Summary ===")
    for entry in task_log:
        print(entry)
    return response

def main():
    client = OpenAI()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://www.bing.com")
        
        response = client.responses.create(
            model="computer-use-preview",
            tools=[{
                "type": "computer_use_preview",
                "display_width": 1024,
                "display_height": 768,
                "environment": "linux"
            }],
            input=[
                {
                  "role": "assistant",
                  "content": """
        You're a Competitive Programming Mentor. You're helping a student on competitive journey. 
        You should suggest problems based on the student's Competitive Programming experience and preferences.
        Student's codeforces rating is 1000.
        With user's rating, prefered tag easy problems, and problem tags 
        (such as dp, greedy, graph, math, etc.) when suggesting problems.
        -open Browser go to a2oj ladder page.
        -click on cancel if it ask for github or username
        -Scroll down to find around 1000 rating codeforces problem, 
        -open the selected problem in new tab.
        -End it after opening tab with required amount of problem."""  
                },
                {
                    "role": "user",
                    "content": "Suggest me one problems"
                }
            ],
            reasoning={
                "generate_summary": "concise",
            },
            truncation="auto"
        )
        
        computer_use_loop(page, client, response)
        browser.close()

if __name__ == "__main__":
    main()