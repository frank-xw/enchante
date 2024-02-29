import os
import requests


def scrape_linkedin_profile(linkedin_profile_url):
    """scrape information from Linkedin profiles
    Manually scrape the information from the Linkedin profile
    """
    debug = os.environ.get("DEBUG_MODE")
    if debug == "True":
        if "linkedin" not in linkedin_profile_url:
            raise Exception(
                f"Wrong Linkedin URL found: {linkedin_profile_url}"
            )
        else:
            gist_url = (
                "https://gist.githubusercontent.com/frank-xw/"
                "6f059210a1c6d9ee9649b6869e1b610a/"
                "raw/07d44364d3fd68466f1ec848a6881cb0b17a07de/andrew-ng.json"
            )
            response = requests.get(gist_url)
            data = response.json()
            profile_pic_url = get_profile_pic_url(linkedin_profile_url)

    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        api_key = os.environ.get("PROXYCURL_API_KEY")
        headers = {"Authorization": "Bearer " + api_key}

        response = requests.get(
            api_endpoint,
            params={"linkedin_profile_url": linkedin_profile_url},
            headers=headers,
        )
        data = response.json()
        profile_pic_url = data.get("profile_pic_url")

    data = {
        key: value
        for key, value in data.items()
        if (
            value not in ([], "", None)
            and key not in ("people_also_viewed", "certifications")
        )
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data, profile_pic_url


def get_profile_pic_url(linkedin_profile_url):
    """Get Linkedin profile picture URL"""
    api_key = os.environ.get("PROXYCURL_API_KEY")
    headers = {"Authorization": "Bearer " + api_key}
    api_endpoint = (
        "https://nubela.co/proxycurl/api/linkedin/person/profile-picture"
    )
    params = {
        "linkedin_person_profile_url": linkedin_profile_url,
    }
    response = requests.get(api_endpoint, params=params, headers=headers)
    profile_pic_url = response.json().get("tmp_profile_pic_url")

    return profile_pic_url


if __name__ == "__main__":
    scrape_linkedin_profile("https://www.linkedin.com/in/andrewyng")
