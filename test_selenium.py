import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

FRONTEND_URL = "http://localhost:8501"
API_URL = "http://127.0.0.1:8000"

def click_sidebar(driver, option):
    wait = WebDriverWait(driver, 10)
    radio = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//label[contains(., '{option}')]")
    ))
    radio.click()
    time.sleep(1.5)


class TestPetRegistry(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.driver.get(FRONTEND_URL)
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

        def setUp(self):
            if FRONTEND_URL not in self.driver.current_url:
                self.driver.get(FRONTEND_URL)
                time.sleep(2)
            else:
                time.sleep(0.5)

    # ──────────────────────────────────────────────────────────────
    # PRUEBA 1 — La app carga correctamente
    # ──────────────────────────────────────────────────────────────
    def test_01_app_loads(self):
        self.driver.get(FRONTEND_URL)
        time.sleep(2)
        self.assertIn("Pet Registry", self.driver.title)
        sidebar = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='stSidebar']")
        ))
        self.assertIsNotNone(sidebar)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("All Pets", body)
        self.assertIn("Register Pet", body)
        print("✅ PRUEBA 1 — App carga correctamente")

    # ──────────────────────────────────────────────────────────────
    # PRUEBA 2 — Navegar a Register Pet
    # ──────────────────────────────────────────────────────────────
    def test_02_navigate_to_register(self):
        click_sidebar(self.driver, "Register Pet")
        time.sleep(1)

        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        inputs[0].clear()
        inputs[0].send_keys("Selenium Dog")
        inputs[1].clear()
        inputs[1].send_keys("dog")
        inputs[2].clear()
        inputs[2].send_keys("Labrador")
        time.sleep(0.5)

        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Register Pet')]")
        ))
        btn.click()
        time.sleep(2)

        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("registered successfully", body)
        print("✅ PRUEBA 2 — Pet creado desde formulario")

    # ──────────────────────────────────────────────────────────────
    # PRUEBA 3 — El pet aparece listado en All Pets
    # ──────────────────────────────────────────────────────────────
    def test_03_pet_appears_in_list(self):
        click_sidebar(self.driver, "All Pets")
        time.sleep(1.5)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Selenium Dog", body)
        self.assertIn("Fixture Dog", body)
        self.assertIn("pet(s) on record", body)
        print("✅ PRUEBA 3 — Ambos pets aparecen en la lista")

    # ──────────────────────────────────────────────────────────────
    # PRUEBA 4 — Actualizar un pet
    # ──────────────────────────────────────────────────────────────
    def test_04_update_pet(self):
        click_sidebar(self.driver, "Update Pet")
        time.sleep(1.5)

        select = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='stSelectbox']")
        ))
        select.click()

        option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(., 'Selenium Dog')]")
        ))
        option.click()

        time.sleep(1)

        # Actualizar nombre
        name_input = self.driver.find_elements(
            By.CSS_SELECTOR,
            "input[type='text']"
        )[0]

        name_input.send_keys(Keys.COMMAND + "a")
        name_input.send_keys(Keys.DELETE)
        name_input.send_keys("Updated Selenium Dog")

        # Actualizar edad
        age_input = self.driver.find_elements(
            By.CSS_SELECTOR,
            "input[type='number']"
        )[0]

        age_input.clear()
        age_input.send_keys("4")

        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Save Changes')]")
        ))

        btn.click()

        time.sleep(2)

        body = self.driver.find_element(By.TAG_NAME, "body").text

        self.assertIn("updated successfully", body)
        self.assertIn("Updated Selenium Dog", body)

        print("✅ PRUEBA 4 — Nombre y edad actualizados correctamente")

    # ──────────────────────────────────────────────────────────────
    # PRUEBA 5 — Formulario rechaza campos vacíos
    # ──────────────────────────────────────────────────────────────
    def test_05_form_validation_empty_fields(self):
        click_sidebar(self.driver, "Register Pet")
        time.sleep(1.5)

        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Register Pet')]")
        ))
        btn.click()
        time.sleep(1.5)

        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("required", body)
        print("✅ PRUEBA 5 — Validación de campos vacíos funciona")

    # ──────────────────────────────────────────────────────────────
    # PRUEBA 6 — Eliminar el pet
    # ──────────────────────────────────────────────────────────────
    def test_06_delete_pet(self):
        self.driver.get(FRONTEND_URL)
        time.sleep(2)

        click_sidebar(self.driver, "Delete Pet")
        time.sleep(1.5)

        select = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='stSelectbox']")
        ))
        select.click()
        time.sleep(0.5)

        option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(., 'Fixture Dog')]")
        ))
        option.click()
        time.sleep(1)

        # Hacer scroll para asegurarse que el checkbox es visible
        checkbox = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='checkbox']")
        ))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        time.sleep(0.5)

        # Usar JavaScript para marcar el checkbox — evita problemas de Streamlit
        self.driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)

        btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Delete Pet')]")
        ))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)

        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Fixture Dog", body)
        self.assertIn("Selenium Dog", body)
        print("✅ PRUEBA 6 — Pet eliminado correctamente")

    # ──────────────────────────────────────────────────────────────
    # PRUEBA 7 — Pet eliminado no aparece en la lista
    # ──────────────────────────────────────────────────────────────
    def test_07_deleted_pet_not_in_list(self):
        click_sidebar(self.driver, "All Pets")
        time.sleep(1.5)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Fixture Dog", body)
        self.assertIn("Updated Selenium Dog", body)
        print("✅ PRUEBA 7 — Fixture Dog eliminado, Selenium Dog intacto")


if __name__ == "__main__":
    unittest.main(verbosity=2)