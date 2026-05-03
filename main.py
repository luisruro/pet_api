from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import uuid4

app = FastAPI()

pets = []

# Pet model
class PetCreate(BaseModel):
    name: str = Field(..., min_length=1)
    species: str = Field(..., min_length=1)
    breed: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)
    gender: str = Field(..., pattern="^(male|female)$")
    comments: Optional[str] = None
    

class Pet(PetCreate):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = datetime.now()


# CRUD endpoints

# List all pets
@app.get("/pets")
async def get_pets():
    return pets

# Create a new pet
@app.post("/pets")
async def create_pet(pet: PetCreate):
    new_pet = Pet(**pet.model_dump())
    pets.append(new_pet)
    return new_pet

# Get a pet by ID
@app.get("/pets/{pet_id}")
async def get_pet(pet_id: str):
    for pet in pets:
        if pet.id == pet_id:
            return pet
    return {"error": "Pet not found"}

# Delete a pet by ID
@app.delete("/pets/{pet_id}")
async def delete_pet(pet_id: str):
    for pet in pets:
        if pet.id == pet_id:
            pets.remove(pet)
            return {"message": "Pet deleted"}
    return {"error": "Pet not found"}

# Update a pet by ID
@app.put("/pets/{pet_id}")
async def update_pet(pet_id: str, pet_update: PetCreate):
    for pet in pets:
        if pet.id == pet_id:
            pet.name = pet_update.name
            pet.species = pet_update.species
            pet.breed = pet_update.breed
            pet.age = pet_update.age
            pet.gender = pet_update.gender
            pet.comments = pet_update.comments
            return pet
    return {"error": "Pet not found"}