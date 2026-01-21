import os
import requests
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")
DATASET_URL = os.getenv("DATASET_URL", "https://static.krevera.com/dataset.json")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
}

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ProductInspection(Base):
    __tablename__ = "product_inspections"

    id = Column(Integer, primary_key=True, index=True)
    molding_machine_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    version = Column(String)
    overall_reject = Column(Boolean)

    # Molding machine state columns
    VtoPTime = Column(Float)
    InjStartPos = Column(Float)
    HoldSegment5PressureSP = Column(Integer)
    VPTransferTimeSP = Column(Integer)
    FillSegment3pressureSP = Column(Integer)
    FillSegment4SP = Column(Integer)
    FillSegmentXfer1to2SP = Column(Float)
    H2TempSP = Column(Integer)
    Barrel5 = Column(Float)
    HoldSegment2PressureSP = Column(Integer)
    BuzzerAlarm = Column(Boolean)
    H1TempSP = Column(Integer)
    EjFwdTimeCV = Column(Float)
    FillSegmentXfer4to5SP = Column(Integer)
    FillSegment4pressureSP = Column(Integer)
    H6TempSP = Column(Integer)
    FillSegment5SP = Column(Integer)
    Barrel2 = Column(Float)
    HoldSegment4TimeSP = Column(Integer)
    PullBackBeforeSP = Column(Integer)
    H3TempSP = Column(Integer)
    Barrel6 = Column(Float)
    HoldSegment1PressureSP = Column(Integer)
    FillSegment2pressureSP = Column(Integer)
    AlarmLED = Column(Boolean)
    ShotCount = Column(Integer)
    FillSegment1SP = Column(Float)
    CushionMin = Column(Float)
    ClampOpenTimeCV = Column(Float)
    ClampCloseTimeCV = Column(Float)
    InjTimeSP = Column(Float)
    HoldSegment3PressureSP = Column(Integer)
    FillSegment3SP = Column(Integer)
    CycleTime = Column(Float)
    N1TempSP = Column(Integer)
    HoldSegment4PressureSP = Column(Integer)
    ClampForceSP = Column(Integer)
    Barrel4 = Column(Float)
    FillSegment5pressureSP = Column(Integer)
    N2TempSP = Column(Integer)
    VtoPPos = Column(Float)
    Barrel1 = Column(Float)
    VtoPPress = Column(Integer)
    H4TempSP = Column(Integer)
    FillSegment2SP = Column(Float)
    HoldSegment1TimeSP = Column(Integer)
    PullBackAfterSP = Column(Integer)
    InjPeakPressure = Column(Integer)
    FillSegmentXfer3to4SP = Column(Integer)
    ChargeTime = Column(Float)
    FillSegmentXfer2to3SP = Column(Integer)
    BarrelN2 = Column(Float)
    TonnageForceCV = Column(Integer)
    CoolTimeSP = Column(Float)
    FillSegment1pressureSP = Column(Integer)
    H5TempSP = Column(Integer)
    FillPeakPress = Column(Integer)
    ShotSizeSP = Column(Float)
    HoldSegment3TimeSP = Column(Integer)
    BarrelN1 = Column(Float)
    CushionFin = Column(Float)
    Barrel3 = Column(Float)
    EjRetTimeCV = Column(Float)
    CycleStopFault = Column(Boolean)
    HoldSegment2TimeSP = Column(Integer)
    VPTransferPositionSP = Column(Float)

    # Object detection columns
    discoloration_defect_reject = Column(Boolean)
    discoloration_defect_pixel_severity_value = Column(Float)
    discoloration_patch_defect_reject = Column(Boolean)
    discoloration_patch_defect_pixel_severity_value = Column(Float)
    flash_defect_reject = Column(Boolean)
    flash_defect_pixel_severity_value = Column(Float)
    short_defect_reject = Column(Boolean)
    short_defect_pixel_severity_value = Column(Float)
    contamination_defect_reject = Column(Boolean)
    contamination_defect_pixel_severity_value = Column(Float)
    splay_defect_reject = Column(Boolean)
    splay_defect_pixel_severity_value = Column(Float)
    burn_mark_defect_reject = Column(Boolean)
    burn_mark_defect_pixel_severity_value = Column(Float)
    jetting_defect_reject = Column(Boolean)
    jetting_defect_pixel_severity_value = Column(Float)
    flow_mark_defect_reject = Column(Boolean)
    flow_mark_defect_pixel_severity_value = Column(Float)
    sink_mark_defect_reject = Column(Boolean)
    sink_mark_defect_pixel_severity_value = Column(Float)
    knit_line_defect_reject = Column(Boolean)
    knit_line_defect_pixel_severity_value = Column(Float)
    void_defect_reject = Column(Boolean)
    void_defect_pixel_severity_value = Column(Float)
    ejector_pin_mark_defect_reject = Column(Boolean)
    ejector_pin_mark_defect_pixel_severity_value = Column(Float)
    label_detection_reject = Column(Boolean)
    label_detection_pixel_severity_value = Column(Float)

def ingest_data():
    response = requests.get(DATASET_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    for entry in data:
        machine_state = entry.get("molding-machine-state", {})
        object_detection = entry.get("object_detection", {})

        inspection_data = {
            "molding_machine_id": entry.get("molding_machine_id"),
            "timestamp": datetime.fromtimestamp(entry.get("timestamp")),
            "version": entry.get("version"),
            "overall_reject": object_detection.get("reject"),
        }

        # Add machine state data
        for key, value in machine_state.items():
            inspection_data[key] = value

        # Add object detection data
        for defect_key, defect_value in object_detection.items():
            if isinstance(defect_value, dict):
                inspection_data[f"{defect_key}_reject"] = defect_value.get("reject")
                pixel_severity = defect_value.get("pixel_severity", {})
                inspection_data[f"{defect_key}_pixel_severity_value"] = pixel_severity.get("value")

        db.add(ProductInspection(**inspection_data))

    db.commit()
    db.close()

if __name__ == "__main__":
    ingest_data()
    print("Data ingestion complete.")
