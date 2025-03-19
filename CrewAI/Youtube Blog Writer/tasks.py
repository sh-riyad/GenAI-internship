from crewai import Task
from tools import yt_tool
from agents import blog_writer, blog_researcher

# Research task
research_task = Task(
    description=(
        "Identify the video {topic},"
        "Get delailed information about the video from the channels"
    ),
    expected_output="A comprehensive 3 paragraph long report based on the {topic} of video content",
    tools=[yt_tool],
    agent=blog_researcher,
)


# Writer task
writer_task = Task(
    description=(
        "Get the info from the youtube on the topic {topic}."
    ),
    expected_output="Summarize the info from the youtube channel video on the topic {topic} and create the content for the blog.",
    tools=[yt_tool],
    agent=blog_writer,
    output_file='new-blog-post.md'
)