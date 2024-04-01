import os
import requests
# from bs4 import BeautifulSoup
import openai
import time

# Replace with your OpenAI secret key
openai.api_key = os.environ.get("OPENAI_API_KEY")
github_token = os.environ.get("GITHUB_TOKEN")

def analyze_repository(repo_url):
    # Fetch repository details from GitHub API
    
    response = requests.get(f"https://api.github.com/repos/{repo_url}")
    repo_data = response.json()
    print(repo_data)

    headers = {"Authorization": f"token {github_token}"}  # Add authorization header
    response = requests.get(f"https://api.github.com/repos/{repo_url}", headers=headers)


    # Extract relevant information (replace with actual fields)
    name = repo_data["name"]
    description = repo_data["description"]
    languages = repo_data["languages"]  # Dictionary with language names and byte counts

    # Combine information for ChatGPT prompt
    prompt = f"This is a GitHub repository called '{name}'.\n"
    prompt += f"Description: {description}\n"
    prompt += "What does this repository do in general?\n"
    prompt += "What programming languages or technologies are used?\n"
    prompt += "Why might someone use this repository?\n"

    # Use ChatGPT API to analyze the repository
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,  # Adjust as needed for response length
        n=1,
        stop=None,
        temperature=0.7,  # Adjust for creativity vs. accuracy
    )

    analysis = response.choices[0].text.strip()
    return analysis

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    analysis = analyze_repository(repo_url)
    print(f"\nAnalysis of '{repo_url}':\n")
    print(analysis)
