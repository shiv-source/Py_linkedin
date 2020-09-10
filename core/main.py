from core.linkedin import Linkedin

user = "Your_Email"
user_pass = "Your_Password"
login_url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
linkedin_url = "https://www.linkedin.com/"
search_quarry = "ceo"
location_quarry = "india"
current_page = 1
last_page = 10

def main():
    obj = Linkedin(username= user , password= user_pass,
        login_url = login_url , linkedin_url=linkedin_url , search_quarry= search_quarry,
        location_quarry=location_quarry , current_page=current_page, last_page=last_page )
    # obj.user_login()
   
    # obj.accept_invitaions()
    obj.search_by_filters()