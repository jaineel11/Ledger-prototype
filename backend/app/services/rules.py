class RulesEngine:
    @staticmethod
    def evaluate_r114(data: dict) -> dict:
        water_class = data.get("water_damage_class")
        prior_claims = data.get("prior_claims_24mo", 0)
        repair_cost = data.get("est_repair_cost", 0)
        coverage = data.get("coverage_limit", 0)

        # GUARDRAIL: Instantly route to human if critical financial data is missing/zero
        if not repair_cost or not coverage or repair_cost <= 0 or coverage <= 0:
            return {
                "decision": "ROUTED_TO_REVIEW",
                "reason": "Missing or invalid financial data. Cannot auto-approve."
            }

        # Original Rule
        if water_class == "Category 2" and prior_claims <= 1 and repair_cost <= coverage:
            return {
                "decision": "APPROVED",
                "reason": "Matched R114, all structural conditions fully satisfied."
            }
        
        return {
            "decision": "ROUTED_TO_REVIEW",
            "reason": "Breach detected: Cost/Limit ratio or Category 3 variance. Human intervention required."
        }