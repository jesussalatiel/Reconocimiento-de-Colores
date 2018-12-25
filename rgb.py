#Librerias necesarias para ejecucion del codigo
import cv2   
import numpy as np
import serial, time

#Variables que necesitan ser modificadas
port_camara = 0
com_arduino = 'COM4'
baudios = 9600 

try:
    #Variable que sera utilizada para enviar el dato por serial
    send_data = b'a'
    #Iniciamos captura de video
    cap=cv2.VideoCapture(port_camara)
    #Puerto para la conexion con Arduino
    arduino = serial.Serial(com_arduino, baudios)
    #Esperamos 2 segundos para  que el programa establesca la conexion serial con arduino
    time.sleep(2)
    print('Conexion establecida con exito.')
    #Se envia 'a' el cual fue establecido en el codigo de arduino como un apagado de led
    arduino.write(b'a')
    #Iniciamos la captura de video
    while(1):
            #Leemos los frames que contiene el video
            _, img = cap.read()            

            #Convertimos la imagen de RGB a HSV
            hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

            #Definimos el rango de colores7
            red_lower=np.array([136,87,111],np.uint8)
            red_upper=np.array([180,255,255],np.uint8)

            #Definimos el rango de colores
            blue_lower=np.array([99,115,150],np.uint8)
            blue_upper=np.array([110,255,255],np.uint8)
            
            #Definimos el rango de colores
            yellow_lower=np.array([22,60,200],np.uint8)
            yellow_upper=np.array([60,255,255],np.uint8)

            #Buscamos el rango de colores que aparecen en la imagen
            red=cv2.inRange(hsv, red_lower, red_upper)
            blue=cv2.inRange(hsv,blue_lower,blue_upper)
            yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)
            #Filtramos el ruido aplicando un open y close
            kernel = np.ones((5 ,5), np.uint8)

            #Marcamos la figura detectada 
            red=  cv2.dilate(red, kernel)
            #Relacionamos las imagenes original y tratada con una etiqueta de distincion para el posterior analisis
            res_red = cv2.bitwise_and(img, img, mask = red)

            blue=  cv2.dilate(blue, kernel)
            res_blue = cv2.bitwise_and(img, img, mask = blue)

            yellow=  cv2.dilate(yellow, kernel)
            res_yellow = cv2.bitwise_and(img, img, mask = yellow)

            #Comparamos en el frame la cantidad de pixeles en rojo para su notificacion 
            _,contours, hierarchy = cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate ( contours):
                area = cv2.contourArea(contour)
                #Si es mayor el area a 300 notificamos el color detectado
                if area > 300:               
                    #Enviamos el caracter de 'r' = rojo por via serial
                    send_data = b'r'
                    #Dibujamos un cuadro en el area que fue detectado el color
                    x,y,w,h = cv2.boundingRect(contour) 
                    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    #Escribimos en pantalla el color 
                    cv2.putText(img,"Rojo",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2,cv2.LINE_AA)
                    
                         
            _,contours, hierarchy = cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate ( contours):
                area = cv2.contourArea(contour)
                if area > 300:
                    send_data = b'b'
                    x,y,w,h = cv2.boundingRect(contour) 
                    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.putText(img,"Azul",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2,cv2.LINE_AA)
                    

            _,contours, hierarchy = cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate ( contours):
                area = cv2.contourArea(contour)
                if area > 300:
                    send_data = b'y'
                    x,y,w,h = cv2.boundingRect(contour) 
                    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
                    cv2.putText(img,"Amarillo",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2,cv2.LINE_AA)
            
            #Enviamos datos por serial                    
            arduino.write(send_data)
            #Establecemos el valor por defecto
            send_data= b'a'
            #Mostramo los frames ya tratado
            cv2.imshow('Deteccion de Colores ', img)

            #cv2.imshow('Deteccion  ', res_red)
            
            #Si presion 'q' el programa es finalizado
            if cv2.waitKey(10) & 0xFF == ord('q'):
                #Liberamos memoria ocupada por OpenCv
                cap.release()
                cv2.destroyAllWindows()
                #Aseguramos que el dispositivo envie señal de apagado
                arduino.write(b'a')
                print('Se ha cerrado la conexión con el dispositivo')
                #Cerramos la conexion serial de arduino
                arduino.close()
                #Salimos del ciclo
                break  
     
except:
    print('Error en la comunicacion.')

    
