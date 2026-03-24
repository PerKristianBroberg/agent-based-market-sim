from dataclasses import dataclass


@dataclass
class Trade:
    round_number: int
    buyer_id: int
    seller_id: int
    price: float
    buyer_reservation: float
    seller_reservation: float

    @property
    def buyer_surplus(self) -> float:
        return self.buyer_reservation - self.price

    @property
    def seller_surplus(self) -> float:
        return self.price - self.seller_reservation

    @property
    def total_surplus(self) -> float:
        return self.buyer_surplus + self.seller_surplus
