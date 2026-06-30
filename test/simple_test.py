from page.AuthPage import AuthPage


def test_first(browser):
    auth_page = AuthPage(browser)
    auth_page.go()
    auth_page.login_as("tanikaqa@gmail.com", "MatrixX-2026_pyr")
