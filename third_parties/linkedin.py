import os
import requests


def scrape_linkedin_profile(linkedin_profile_url, test_mode=True):
    """scrape information from Linkedin profiles
    Manually scrape the information from the Linkedin profile
    """
    if test_mode:
        gist_url = "https://gist.githubusercontent.com/frank-xw/"\
            "6f059210a1c6d9ee9649b6869e1b610a/"\
            "raw/07d44364d3fd68466f1ec848a6881cb0b17a07de/andrew-ng.json"
        response = requests.get(gist_url)
        return response

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    api_key = os.environ.get("PROXYCURL_API_KEY")
    headers = {"Authorization": "Bearer " + api_key}

    response = requests.get(
        api_endpoint,
        params={"linkedin_profile_url": linkedin_profile_url},
        headers=headers,
    )

    return print(response)


if __name__ == "__main__":
    print(scrape_linkedin_profile("test").json())
