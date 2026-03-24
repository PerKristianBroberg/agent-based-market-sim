import random
from typing import Optional
from agents.buyer import Buyer
from agents.seller import Seller
from market.trade import Trade


class Market:
    """
    Matches one random buyer with one random seller per round.
    Trade occurs if buyer's offer >= seller's offer.
    Price is set at the midpoint.
    """

    def __init__(self, buyers: list[Buyer], sellers: list[Seller]):
        self.buyers = buyers
        self.sellers = sellers
        self.trade_history: list[Trade] = []

    def run_round(self, round_number: int) -> Optional[Trade]:
        buyer = random.choice(self.buyers)
        seller = random.choice(self.sellers)

        buyer_offer = buyer.get_offer()
        seller_offer = seller.get_offer()

        if buyer_offer >= seller_offer:
            price = (buyer_offer + seller_offer) / 2
            trade = Trade(
                round_number=round_number,
                buyer_id=buyer.agent_id,
                seller_id=seller.agent_id,
                price=price,
                buyer_reservation=buyer.reservation_price,
                seller_reservation=seller.reservation_price,
            )
            buyer.record_trade(price)
            seller.record_trade(price)
            self.trade_history.append(trade)
            buyer.on_round_end(traded=True)
            seller.on_round_end(traded=True)
            return trade

        buyer.on_round_end(traded=False)
        seller.on_round_end(traded=False)
        return None
