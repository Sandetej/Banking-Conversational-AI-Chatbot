"""Dialogue templates for synthetic data."""

DIALOGUE_TEMPLATES = {
    "get_balance": {
        "single_turn": [
            "What is my account balance?",
            "Show me my balance",
            "How much money do I have?",
            "Check my checking account",
        ]
    },
    "transaction_history": {
        "single_turn": [
            "Show my recent transactions",
            "List my transactions from last week",
            "What did I spend?",
            "Show transactions from Aug 1-15",
        ]
    },
    "lost_or_stolen_card": {
        "single_turn": [
            "I lost my card",
            "My card was stolen",
            "Report lost card",
            "I can't find my card",
        ]
    },
    "transfer_money": {
        "single_turn": [
            "Transfer 500 to savings",
            "Send money to my other account",
            "Move money between accounts",
        ]
    },
    "card_not_working": {
        "single_turn": [
            "My card isn't working",
            "Card declined",
            "Why won't my card work",
        ]
    },
    "activate_my_card": {
        "single_turn": [
            "Activate my card",
            "How do I activate my new card",
        ]
    },
    "change_pin": {
        "single_turn": [
            "Change my PIN",
            "Update card PIN",
        ]
    },
    "exchange_rate": {
        "single_turn": [
            "What is the exchange rate",
            "USD to EUR rate",
        ]
    },
    "atm_support": {
        "single_turn": [
            "Where is the nearest ATM",
            "ATM locations near me",
        ]
    },
    "disputed_transaction": {
        "single_turn": [
            "I don't recognize this charge",
            "This charge is wrong",
            "Dispute a transaction",
        ]
    },
}

SIMPLE_INTENTS = [
    "card_about_to_expire", "card_arrival", "card_delivery_estimate",
    "card_acceptance", "card_payment_fee_charged", "compromised_card",
    "cancel_transfer", "transfer_timing", "transfer_fee_charged",
    "transfer_not_received_by_recipient", "declined_transfer", "failed_transfer",
    "pending_transfer", "top_up_failed", "balance_not_updated_after_bank_transfer",
    "pending_top_up", "pending_card_payment", "exchange_charge", "extra_charge_on_statement",
    "verify_my_identity", "passcode_forgotten", "apple_pay_or_google_pay",
    "contactless_not_working", "supported_cards_and_currencies", "get_physical_card",
    "edit_personal_details", "order_physical_card", "pin_blocked", "terminate_account",
    "request_refund", "transaction_history", "status_tracking_general", "explain_banking_terms"
]
