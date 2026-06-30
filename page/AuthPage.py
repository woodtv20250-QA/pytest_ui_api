from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class AuthPage:

    def __init__(self, driver: WebDriver) -> None:
        self.__url = "https://www.kinopoisk.ru/"
        self.__driver = driver

    def go(self):
        self.__driver.get(self.__url)

    def get_current_url(self) -> str:
        return self.__driver.current_url

    def login_as(self, email: str, password: str):

        # 1. Нажать "Войти"
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "button.styles_loginButton__6_QNl"))
        ).click()
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR,
                '[data-testid="split-add-user-more-button"]')))

        # 2. Нажать "Ещё"
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '[data-testid="split-add-user-more-button"]'))
        ).click()
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, '[data-testid="menu-option-switchToLogin"]')))

        # 3. Выбрать "Войти по логину"
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '[data-testid=menu-option-switchToLogin]'))
        ).click()

        # 4. Ввести логин
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, '[aria-label="Логин или email"]')))
        login_field = self.__driver.find_element(
            By.CSS_SELECTOR, '[aria-label="Логин или email"]')
        login_field.clear()
        login_field.send_keys(email)

        # 5. Нажать "Войти"
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '[data-testid="split-add-user-next-login"]'))
        ).click()

        # 6. Ввести пароль
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, '[placeholder="Пароль"]'))
        )
        password_field = self.__driver.find_element(
            By.CSS_SELECTOR, '[placeholder="Пароль"]')
        password_field.clear()
        password_field.send_keys(password)

        # 7. Нажать "Далее"
        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, '[data-testid="password-next"]'))).click()

        # Обработка попапа "Просто входите в аккаунт"
        try:
            WebDriverWait(self.__driver, 5).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    '[data-testid="webauthn-reg-agree-button"]')))

            # Пробуем нажать "Напомнить позже"
            try:
                WebDriverWait(self.__driver, 3).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        '[data-testid="webauthn-reg-later-button"]'))).click()
                print("Попап закрыт кнопкой 'Напомнить позже'")
            except TimeoutException:
                # Если нет "Напомнить позже" - нажимаем "Давайте!"
                WebDriverWait(self.__driver, 3).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        '[data-testid="webauthn-reg-agree-button"]'))).click()
                print("Попап закрыт кнопкой 'Давайте!'")
        except TimeoutException:
            print("Попап не появился")
            pass

        # 8. Проверяем, запрошен ли код
        try:
            WebDriverWait(self.__driver, 5).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR, '[aria-label="code from email"]')))
            print("Код запрошен. Ожидание ввода...")

            self.__driver.save_screenshot("code_required.png")

            print("\n" + "="*60)
            print("Требуется ввод кода подтверждения")
            print("Перейдите в почтовый ящик, скопируйте код")
            print("Вставьте код в поле ввода в браузере")
            print("После ввода кода нажмите Enter в терминале")
            print("="*60)

            input()

            try:
                WebDriverWait(self.__driver, 10).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        '[data-testid="webauthn-reg-later-button"]'))).click()
            except TimeoutException:
                pass
            WebDriverWait(self.__driver, 15).until(
                EC.url_contains("kinopoisk.ru"))
            WebDriverWait(self.__driver, 5).until(
                EC.url_changes("https://passport.yandex.ru/auth"))
        except TimeoutException:
            WebDriverWait(self.__driver, 10).until(
                EC.url_contains("kinopoisk.ru"))
            WebDriverWait(self.__driver, 5).until(
                EC.url_changes("https://passport.yandex.ru/auth"))

        current_url = self.get_current_url()
        assert "kinopoisk.ru" in current_url, "Не удалось перейти на Кинопоиск"
        assert (
            "passport.yandex.ru" not in current_url
        ), "Страница авторизации не закрыта"
