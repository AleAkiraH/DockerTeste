FROM tiangolo/uwsgi-nginx-flask:python3.6
RUN pip install Flask
RUN pip install cmake
RUN pip install dlib
RUN pip install opencv-python
RUN pip install imutils
RUN pip install face_recognition