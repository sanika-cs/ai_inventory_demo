# Copyright (c) 2025, sanika and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ai_inventory_demo.ai_inventory_demo.utils.ml_client import get_ml_client

class inventorydemoprediction(Document):
    def validate(self):
        self.get_prediction()
    
    def get_prediction(self):
        try:
            # Get prediction from ML service
            ml_client = get_ml_client()
            result = ml_client.get_prediction(
                item_code=self.item_code,
                warehouse=self.warehouse,
                company=self.company
            )
            
            # Update document with prediction results
            self.predicted_quantity = result.get("predicted_quantity", 0)
            self.confidence_score = result.get("confidence_score", 0)
            
        except Exception as e:
            frappe.log_error(f"Error in inventory prediction: {str(e)}")
            frappe.throw("Error getting prediction. Please check the logs.")
