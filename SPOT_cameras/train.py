from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolo11n.pt") 
    data_path = r'C:/prctm_dog/SPOT_cameras/pistolero/data.yaml'
    
    train_results = model.train(
        data=data_path,
        epochs=10,
        imgsz=640,
        device='cpu',
        )