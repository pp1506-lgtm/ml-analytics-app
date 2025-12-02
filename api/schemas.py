from pydantic import BaseModel
from typing import List, Optional

class ChurnRequest(BaseModel):
    seniorcitizen: int
    partner: int
    dependents: int
    tenure: int
    phoneservice: int
    multiplelines: int
    onlinesecurity: int
    onlinebackup: int
    deviceprotection: int
    techsupport: int
    streamingtv: int
    streamingmovies: int
    paperlessbilling: int
    monthlycharges: float
    totalcharges: float
    gender_male: int
    internetservice_fiber_optic: int
    internetservice_no: int
    contract_one_year: int
    contract_two_year: int
    paymentmethod_credit_card_automatic: int
    paymentmethod_electronic_check: int
    paymentmethod_mailed_check: int


class BatchChurnRequest(BaseModel):
    records: List[ChurnRequest]
