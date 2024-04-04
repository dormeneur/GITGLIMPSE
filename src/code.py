import os
import time
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = openai_api_key)

def analyze_repository(repo_url):
    headers = {"Authorization": f"token {github_token}"}
    time.sleep(2)
    max_retries = 3
    initial_delay = 1
    endpoints = repo_url.split("/")[-2] + "/" + repo_url.split("/")[-1]

    for attempt in range(max_retries):
        response = requests.get(f"https://api.github.com/repos/{endpoints}", headers=headers)
        if response.status_code == 200:
            repo_data = response.json()
            #print(repo_data)
            if "full_name" in repo_data:
                name = repo_data["full_name"]
                #print("name: ", name)
            else:
                print("Error: Could not find repository name in response data.")
                return None
            
            description = repo_data.get("description", "No description provided.")
            languages = repo_data.get("language", "Unknown")
            prompt = f"This is a GitHub repository called '{name}'.\n"
            prompt += f"Description: {description}\n"
            prompt += f"Programming Language: {languages}\n"
            prompt += "What does this repository do in general?\n"
            prompt += "Why might someone use this repository?\n"

            try:
                response = client.completions.create(model = "davinci-002", prompt = prompt)
            except:
                print("\nEither of the two things happend:\n  1. You don't have sufficient quota for this model today.\n  2. You're broke and don't have access to this GPT text model.\n...and that's why I can't even complete a single project\n")
                exit()

            analysis = response.choices[0].text.strip()
            return analysis

        elif response.status_code == 403:
            print("Rate limit exceeded. Retrying...")
            delay = initial_delay * 2**attempt
            time.sleep(delay)

    print(f"Error: Unexpected response status code: {response.status_code}")
    return None


if __name__ == "__main__":

    repo_url = input("Enter the GitHub repository URL: ")
    analysis = analyze_repository(repo_url)

    if analysis:
        print(f"\nAnalysis of '{repo_url}':\n")
        print(analysis)
    else:
        print("An error occurred. Please check the previous messages for details.")
