import json
from datetime import datetime

class Reporter:
    """Generate audit reports"""
    
    def create_report(self, user_id, scan_results):
        """Create audit report from scan results"""
        report = {
            "user_id": str(user_id),
            "timestamp": datetime.now().isoformat(),
            "scan_results": scan_results,
            "summary": self._create_summary(scan_results)
        }
        return report
    
    def format_report(self, report):
        """Format report as string"""
        output = f"""
╔════════════════════════════════════════╗
║  🛡️  SECURITY AUDIT REPORT  🛡️        ║
╚════════════════════════════════════════╝

Generated: {report['timestamp']}
User ID: {report['user_id']}

📊 SUMMARY:
{self._format_summary(report['summary'])}

📝 DETAILS:
{json.dumps(report['scan_results'], indent=2)}

---
Remember: Keep your secrets safe!
Never share tokens, passwords, or keys.
"""
        return output
    
    def _create_summary(self, results):
        """Create summary statistics"""
        return {
            "total_items_found": len(results),
            "categories": list(set(r.get('type', 'unknown') for r in results if isinstance(r, dict)))
        }
    
    def _format_summary(self, summary):
        """Format summary for display"""
        text = f"Total items found: {summary['total_items_found']}\n"
        text += f"Categories: {', '.join(summary['categories'])}"
        return text
