"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
   "Clube de Xadrez": {
      "description": "Aprenda estratégias e participe de torneios de xadrez",
      "schedule": "Sextas, 15h30 - 17h",
      "max_participants": 12,
      "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
   },
   "Aula de Programação": {
      "description": "Aprenda fundamentos de programação e desenvolva projetos de software",
      "schedule": "Terças e quintas, 15h30 - 16h30",
      "max_participants": 20,
      "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
   },
   "Educação Física": {
      "description": "Educação física e atividades esportivas",
      "schedule": "Segundas, quartas e sextas, 14h - 15h",
      "max_participants": 30,
      "participants": ["john@mergington.edu", "olivia@mergington.edu"]
   },
   # Esportivas
   "Treino de Basquete": {
      "description": "Fundamentos, táticas e partidas amistosas de basquete",
      "schedule": "Terças e quintas, 16h30 - 18h",
      "max_participants": 15,
      "participants": ["marcos@mergington.edu"]
   },
   "Aula de Natação": {
      "description": "Técnicas de nado e condicionamento físico na piscina",
      "schedule": "Quartas, 15h - 16h30",
      "max_participants": 18,
      "participants": ["laura@mergington.edu", "felipe@mergington.edu"]
   },
   # Artísticas
   "Clube de Teatro": {
      "description": "Interpretação, improvisação e produção de peças",
      "schedule": "Segundas e quartas, 16h - 17h30",
      "max_participants": 25,
      "participants": ["isabela@mergington.edu"]
   },
   "Oficina de Pintura": {
      "description": "Exploração de técnicas de pintura e artes visuais",
      "schedule": "Sextas, 14h - 15h30",
      "max_participants": 20,
      "participants": ["carlos@mergington.edu", "marina@mergington.edu"]
   },
   # Intelectuais
   "Clube de Matemática": {
      "description": "Resolução de problemas, lógica e preparação para olimpíadas",
      "schedule": "Terças, 14h - 15h30",
      "max_participants": 16,
      "participants": ["helena@mergington.edu"]
   },
   "Laboratório de Ciências": {
      "description": "Experimentos práticos e exploração científica",
      "schedule": "Quintas, 15h - 16h30",
      "max_participants": 22,
      "participants": ["gabriel@mergington.edu", "sofia@mergington.edu"]
   }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    activity = activities[activity_name]

    # Validar se já inscrito
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Estudante já inscrito")

    # Validar capacidade
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Atividade cheia")

    activity["participants"].append(email)
    return {"message": f"{email} inscrito(a) em {activity_name} com sucesso"}
