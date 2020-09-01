from core.linkedin import Linkedin

user = USER_EMAIL
user_pass = USER_PASSWORD
login_url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"


def main():
    obj = Linkedin(username= user , password= user_pass,
        login_url = login_url , linkedin_url=linkedin_url )
    #obj.user_login()
    obj.accept_invitaions()