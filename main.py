from fastapi import FastAPI, File
from segmentation import get_yolov5, get_image_from_bytes
from starlette.responses import Response
import io
from PIL import Image
import json
from fastapi.middleware.cors import CORSMiddleware
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException 
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fastapi.responses import FileResponse 
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse

model = get_yolov5()

app = FastAPI(
    title="Custom YOLOV5 Machine Learning API",
    description="""Obtain object value out of image
                    and return image and json result""",
    version="0.0.1",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/object-to-json")
async def detect_food_return_json_result(file: bytes = File(...)):
    input_image = get_image_from_bytes(file)
    results = model(input_image)
    detect_res = results.pandas().xyxy[0].to_json(orient="records")  # JSON img1 predictions
    detect_res = json.loads(detect_res)
    return {"result": detect_res}


@app.post("/object-to-img")
async def detect_food_return_base64_img(file: bytes = File(...)):
    input_image = get_image_from_bytes(file)
    print("input_image =>", input_image)
    results = model(input_image)
    print("results =>", results)
    a = results.render()  # updates results.imgs with boxes and labels
    print("a =>", a)
    for img in a:
        print('img', img)
        bytes_io = io.BytesIO()
        img_base64 = Image.fromarray(img)
        img_base64.save(bytes_io, format="jpeg")
    return Response(content=bytes_io.getvalue(), media_type="image/jpeg") 

@app.post("/convert_image/")
async def convert_image(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        encoded_image = base64.b64encode(file_bytes).decode('utf-8')
        return {"base64_encoded_image": encoded_image}
    except Exception as e:
        return {"error": str(e)}

@app.post("/decode_image/")
async def decode_image(image_file: UploadFile = File(...), json_file: UploadFile = File(...)):
    try:
        # Đọc nội dung của tệp hình ảnh và tệp JSON
        image_content = await image_file.read()
        json_content = await json_file.read()

        # Giải mã nội dung JSON thành từ điển Python
        data = json.loads(json_content.decode())
        data1 = json.loads(image_content.decode())

        # Lấy chuỗi base64 hình ảnh và thông tin bounding box từ dữ liệu JSON
        encoded_image = data.get("base64_encoded_image", "")
        bounding_boxes = data1.get("result", [])

        if not encoded_image:
            raise HTTPException(status_code=400, detail="Nội dung JSON không hợp lệ. Thiếu trường 'base64_encoded_image'.")

        # Tạo hình ảnh từ chuỗi base64
        image_bytes = base64.b64decode(encoded_image)

        # Pass the image through the get_image_from_bytes function
        input_image = get_image_from_bytes(image_bytes)

        # Draw bounding boxes on the image
        for bbox in bounding_boxes:
            x_min = int(bbox["xmin"])
            y_min = int(bbox["ymin"])
            x_max = int(bbox["xmax"])
            y_max = int(bbox["ymax"])

            # Draw bounding box as a rectangle
            ImageDraw.Draw(input_image).rectangle([x_min, y_min, x_max, y_max], outline="red", width=5)

        # Save the modified image to a bytes buffer
        img_byte_array = io.BytesIO()
        input_image.save(img_byte_array, format="PNG")
        img_byte_array = img_byte_array.getvalue()

        # Return the image as a StreamingResponse
        return StreamingResponse(io.BytesIO(img_byte_array), media_type="image/png")

    except Exception as e:
        return {"error": str(e)}