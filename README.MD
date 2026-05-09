# INSTRUCTIONS

## Run using `uv`

### You must Install `Python` (if you don’t have it)

### You must Install `uv` (if you don’t have it)

Using **Git Bash**, Linux, or macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Restart your terminal after installation.

### Install dependencies

```bash
uv sync
```
### Run Backend

```bash
fastapi dev
```

### Run Frontend

```bash
uv run streamlit run app.py
```

### Run Selenium Test

```bash
uv run test_selenium.py
```

## API Reference

### POST `/pets`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | ✅ | Min 1 character |
| `species` | string | ✅ | Min 1 character |
| `breed` | string | ✅ | Min 1 character |
| `age` | integer | ✅ | Must be greater than 0 |
| `gender` | string | ✅ | `male` or `female` only |
| `comments` | string | ❌ | Optional notes |

**Example — minimal:**
```json
{
  "name": "Max",
  "species": "Dog",
  "breed": "Labrador",
  "age": 3,
  "gender": "male"
}
```

**Example — complete:**
```json
{
  "name": "Luna",
  "species": "Cat",
  "breed": "Siamese",
  "age": 2,
  "gender": "female",
  "comments": "Vaccinated, very calm indoors"
}
```



