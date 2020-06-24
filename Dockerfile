FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY ./app /app
RUN pip install Flask
RUN pip install cmake
RUN pip install dlib
RUN pip install opencv-python
RUN pip install imutils
RUN pip install face_recognition