import logging

from fastapi import FastAPI, Form, File, UploadFile

from controllers.chatbot_controller import ChatBotController

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    chatbot_controller = ChatBotController()
    chatbot_controller.initialize()


@app.post("/uploadCustomDoc/")
async def upload_custom_doc(file: UploadFile = File(...)):
    with open(file.filename, "wb") as file_object:
        file_object.write(file.file.read())

    chatbot_controller = ChatBotController()
    await chatbot_controller.add_document(file.filename, file.content_type)
    return {"filename": file.filename}


@app.post("/uploadCustomDocs/")
async def upload_custom_docs(files: list[UploadFile] = File(...)):
    chatbot_controller = ChatBotController()
    filenames = []
    for file in files:
        with open(file.filename, "wb") as file_object:
            file_object.write(file.file.read())

        await chatbot_controller.add_document(file.filename, file.content_type)
        filenames.append(file.filename)
    return {"filenames": filenames}
