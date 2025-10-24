import frappe
import requests
import json
from typing import Dict, Any

class MLClient:
    def __init__(self):
        # Get ML service URL from site config or default to demo URL
        self.ml_service_url = frappe.conf.get('ml_service_url', 'http://your-ml-service-url')
    
    def get_prediction(self, item_code: str, warehouse: str, company: str) -> Dict[str, Any]:
        """
        Get inventory prediction from ML service
        
        Args:
            item_code: Item code to predict for
            warehouse: Warehouse code
            company: Company code
            
        Returns:
            Dict containing prediction results with keys:
            - predicted_quantity: float
            - confidence_score: float
        """
        try:
            # Prepare data payload
            data = {
                "item_code": item_code,
                "warehouse": warehouse,
                "company": company,
                # You can add more data points here that your ML model needs
                # Example:
                # "historical_data": get_historical_data(item_code, warehouse)
            }
            
            # Make request to ML service
            response = requests.post(
                f"{self.ml_service_url}/predict",
                json=data,
                headers={
                    "Content-Type": "application/json",
                    # Add any required API keys or auth headers
                    # "Authorization": f"Bearer {frappe.conf.get('ml_service_api_key')}"
                },
                timeout=30  # 30 second timeout
            )
            
            response.raise_for_status()  # Raise exception for non-200 status codes
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            frappe.log_error(
                f"ML Service Request Failed: {str(e)}",
                "Inventory Prediction Error"
            )
            raise
            
        except Exception as e:
            frappe.log_error(
                f"ML Prediction Error: {str(e)}",
                "Inventory Prediction Error"
            )
            raise

def get_ml_client() -> MLClient:
    """
    Factory function to get MLClient instance
    """
    return MLClient()