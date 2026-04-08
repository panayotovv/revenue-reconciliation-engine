import csv

def export_results(results, output_file):

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["order_id", "email", "amount", "status", "confidence", "payment_id"])

        for r in results:
            writer.writerow([
                r["order_id"],
                r["email"],
                r["amount"],
                r["status"],
                r["confidence"],
                r["payment_id"]
            ])