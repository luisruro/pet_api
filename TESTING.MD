# 🧪 Testing — Pet Registry API

Guía de pruebas manuales con Postman para todos los endpoints de la API.

> **Base URL:** `http://127.0.0.1:8000`  
> **Variable compartida:** `{{pet_id}}` — se guarda automáticamente al ejecutar la prueba **POST 1.1**

---

## Orden de ejecución recomendado

```
1. POST /pets          → crea el pet y guarda {{pet_id}}
2. GET  /pets          → lista todos los pets
3. GET  /pets/:id      → obtiene el pet creado
4. PUT  /pets/:id      → actualiza el pet
5. DELETE /pets/:id    → elimina el pet
```

---

## 1. POST /pets — Crear un pet

### 1.1 Crear pet válido con todos los campos

**URL**
```
POST http://127.0.0.1:8000/pets
```

**Body (JSON)**
```json
{
  "name": "Buddy",
  "species": "dog",
  "breed": "Labrador",
  "age": 3,
  "gender": "male",
  "comments": "Muy amigable"
}
```

**Tests**
```javascript
pm.test("Status 200 OK", function() {
    pm.response.to.have.status(200);
});

pm.test("El pet retornado tiene los datos enviados", function() {
    var pet = pm.response.json();
    pm.expect(pet.name).to.eql("Buddy");
    pm.expect(pet.species).to.eql("dog");
    pm.expect(pet.breed).to.eql("Labrador");
    pm.expect(pet.age).to.eql(3);
    pm.expect(pet.gender).to.eql("male");
    pm.expect(pet.comments).to.eql("Muy amigable");
});

pm.test("Se generó un ID en formato UUID", function() {
    var pet = pm.response.json();
    pm.expect(pet.id).to.be.a("string");
    pm.expect(pet.id).to.match(/^[0-9a-f-]{36}$/);
});

pm.test("Se generó el campo created_at", function() {
    var pet = pm.response.json();
    pm.expect(pet.created_at).to.be.a("string");
});

// Guardar el ID para pruebas siguientes
var pet = pm.response.json();
pm.collectionVariables.set("pet_id", pet.id);
console.log("pet_id guardado:", pet.id);
```

---

### 1.2 Crear pet sin campo comments (opcional)

**URL**
```
POST http://127.0.0.1:8000/pets
```

**Body (JSON)**
```json
{
  "name": "Luna",
  "species": "cat",
  "breed": "Siamese",
  "age": 2,
  "gender": "female"
}
```

**Tests**
```javascript
pm.test("Status 200 OK", function() {
    pm.response.to.have.status(200);
});

pm.test("El campo comments es null cuando no se envía", function() {
    var pet = pm.response.json();
    pm.expect(pet.comments).to.be.null;
});
```

---

### 1.3 Crear pet sin campo name (requerido)

**URL**
```
POST http://127.0.0.1:8000/pets
```

**Body (JSON)**
```json
{
  "species": "dog",
  "breed": "Poodle",
  "age": 1,
  "gender": "male"
}
```

**Tests**
```javascript
pm.test("Status 422 Unprocessable Entity", function() {
    pm.response.to.have.status(422);
});

pm.test("El error menciona el campo name", function() {
    var body = pm.response.json();
    var detail = JSON.stringify(body.detail);
    pm.expect(detail).to.include("name");
});
```

---

### 1.4 Crear pet con age = 0 (debe ser mayor que 0)

**URL**
```
POST http://127.0.0.1:8000/pets
```

**Body (JSON)**
```json
{
  "name": "Rex",
  "species": "dog",
  "breed": "Boxer",
  "age": 0,
  "gender": "male"
}
```

**Tests**
```javascript
pm.test("Status 422 — age 0 no es válida (gt=0)", function() {
    pm.response.to.have.status(422);
});
```

---

### 1.5 Crear pet con gender inválido

**URL**
```
POST http://127.0.0.1:8000/pets
```

**Body (JSON)**
```json
{
  "name": "Max",
  "species": "dog",
  "breed": "Husky",
  "age": 4,
  "gender": "unknown"
}
```

**Tests**
```javascript
pm.test("Status 422 — gender debe ser male o female", function() {
    pm.response.to.have.status(422);
});

pm.test("El error menciona el campo gender", function() {
    var body = pm.response.json();
    var detail = JSON.stringify(body.detail);
    pm.expect(detail).to.include("gender");
});
```

---

## 2. GET /pets — Listar todos los pets

### 2.1 Listar pets con datos registrados

**URL**
```
GET http://127.0.0.1:8000/pets
```

**Tests**
```javascript
pm.test("Status 200 OK", function() {
    pm.response.to.have.status(200);
});

pm.test("Cada pet tiene los campos requeridos", function() {
    var pets = pm.response.json();
    if (pets.length > 0) {
        pm.expect(pets[0]).to.have.property("id");
        pm.expect(pets[0]).to.have.property("name");
        pm.expect(pets[0]).to.have.property("species");
        pm.expect(pets[0]).to.have.property("breed");
        pm.expect(pets[0]).to.have.property("age");
        pm.expect(pets[0]).to.have.property("gender");
        pm.expect(pets[0]).to.have.property("created_at");
    }
});

pm.test("El campo gender es male o female", function() {
    var pets = pm.response.json();
    pets.forEach(function(pet) {
        pm.expect(pet.gender).to.be.oneOf(["male", "female"]);
    });
});
```

---

## 3. GET /pets/{id} — Obtener pet por ID

### 3.1 Obtener pet existente por ID

**URL**
```
GET http://127.0.0.1:8000/pets/{{pet_id}}
```

**Tests**
```javascript
pm.test("Status 200 OK", function() {
    pm.response.to.have.status(200);
});

pm.test("El pet retornado corresponde al ID solicitado", function() {
    var pet = pm.response.json();
    var petId = pm.collectionVariables.get("pet_id");
    pm.expect(pet.id).to.eql(petId);
});

pm.test("El pet tiene todos los campos esperados", function() {
    var pet = pm.response.json();
    pm.expect(pet).to.have.property("id");
    pm.expect(pet).to.have.property("name");
    pm.expect(pet).to.have.property("species");
    pm.expect(pet).to.have.property("breed");
    pm.expect(pet).to.have.property("age");
    pm.expect(pet).to.have.property("gender");
    pm.expect(pet).to.have.property("created_at");
});
```

---

### 3.2 Obtener pet con ID inexistente

**URL**
```
GET http://127.0.0.1:8000/pets/00000000-0000-0000-0000-000000000000
```

**Tests**
```javascript
pm.test("Status 404 Not Found", function() {
    pm.response.to.have.status(404);
});

pm.test("La respuesta contiene un mensaje de error", function() {
    var body = pm.response.json();
    pm.expect(body).to.have.property("error");
    pm.expect(body.error).to.include("not found");
});
```

---

## 4. PUT /pets/{id} — Actualizar pet

### 4.1 Actualizar todos los campos de un pet existente

**URL**
```
PUT http://127.0.0.1:8000/pets/{{pet_id}}
```

**Body (JSON)**
```json
{
  "name": "Buddy Updated",
  "species": "dog",
  "breed": "Golden Retriever",
  "age": 4,
  "gender": "male",
  "comments": "Ahora tiene 4 años"
}
```

**Tests**
```javascript
pm.test("Status 200 OK", function() {
    pm.response.to.have.status(200);
});

pm.test("Los datos fueron actualizados correctamente", function() {
    var pet = pm.response.json();
    pm.expect(pet.name).to.eql("Buddy Updated");
    pm.expect(pet.breed).to.eql("Golden Retriever");
    pm.expect(pet.age).to.eql(4);
    pm.expect(pet.comments).to.eql("Ahora tiene 4 años");
});

pm.test("El ID no cambia al actualizar", function() {
    var pet = pm.response.json();
    var petId = pm.collectionVariables.get("pet_id");
    pm.expect(pet.id).to.eql(petId);
});
```

---

### 4.2 Actualizar pet con ID inexistente

**URL**
```
PUT http://127.0.0.1:8000/pets/00000000-0000-0000-0000-000000000000
```

**Body (JSON)**
```json
{
  "name": "Ghost",
  "species": "cat",
  "breed": "Unknown",
  "age": 1,
  "gender": "male"
}
```

**Tests**
```javascript
pm.test("Status 404 Not Found", function() {
    pm.response.to.have.status(404);
});

pm.test("La respuesta contiene un mensaje de error", function() {
    var body = pm.response.json();
    pm.expect(body).to.have.property("error");
    pm.expect(body.error).to.include("not found");
});
```

---

### 4.3 Actualizar con age negativo

**URL**
```
PUT http://127.0.0.1:8000/pets/{{pet_id}}
```

**Body (JSON)**
```json
{
  "name": "Buddy",
  "species": "dog",
  "breed": "Labrador",
  "age": -1,
  "gender": "male"
}
```

**Tests**
```javascript
pm.test("Status 422 — datos inválidos rechazados en update", function() {
    pm.response.to.have.status(422);
});
```

---

## 5. DELETE /pets/{id} — Eliminar pet

### 5.1 Eliminar pet con ID inexistente (ejecutar primero)

**URL**
```
DELETE http://127.0.0.1:8000/pets/00000000-0000-0000-0000-000000000000
```

**Tests**
```javascript
pm.test("Status 404 Not Found", function() {
    pm.response.to.have.status(404);
});

pm.test("La respuesta contiene un mensaje de error", function() {
    var body = pm.response.json();
    pm.expect(body).to.have.property("error");
    pm.expect(body.error).to.include("not found");
});
```

---

### 5.2 Eliminar pet existente

**URL**
```
DELETE http://127.0.0.1:8000/pets/{{pet_id}}
```

**Tests**
```javascript
pm.test("Status 200 OK", function() {
    pm.response.to.have.status(200);
});

pm.test("La respuesta confirma la eliminación", function() {
    var body = pm.response.json();
    pm.expect(body).to.have.property("message");
    pm.expect(body.message).to.include("deleted");
});
```

---

### 5.3 Eliminar el mismo pet dos veces (idempotencia)

**URL**
```
DELETE http://127.0.0.1:8000/pets/{{pet_id}}
```

**Tests**
```javascript
pm.test("Status 404 Not Found", function() {
    pm.response.to.have.status(404);
});

pm.test("Retorna error al intentar eliminar un pet ya eliminado", function() {
    var body = pm.response.json();
    pm.expect(body).to.have.property("error");
    pm.expect(body.error).to.include("not found");
});
```

---

### 5.4 Verificar que el pet eliminado ya no existe en la lista

**URL**
```
GET http://127.0.0.1:8000/pets
```

**Tests**
```javascript
pm.test("Status 200 OK", function() {
    pm.response.to.have.status(200);
});

pm.test("El pet eliminado no aparece en la lista", function() {
    var pets = pm.response.json();
    var petId = pm.collectionVariables.get("pet_id");
    var found = pets.find(function(p) { return p.id === petId; });
    pm.expect(found).to.be.undefined;
});
```