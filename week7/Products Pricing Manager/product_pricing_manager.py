import logging

SEPARATOR_LINE = "=" * 90
DIVIDER_LINE = "-" * 90

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("week7/Products Pricing Manager/activity_log.log"),
        logging.StreamHandler()                  
    ]
)
def get_discount(prod_category, user_tier):
    
    cat_rates = {
        'Electronics': 10,
        'Clothing': 15,
        'Books': 5,
        'Home': 12
    }
    
    tier_rates = {
        'Premium': 5,
        'Standard': 0,
        'Budget': 2
    }

    base_rate = cat_rates.get(prod_category, 0)
    bonus_rate = tier_rates.get(user_tier, 0)

    return base_rate + bonus_rate

def generate_pricing_sheet(source_path, dest_path):
    
    processed_items = []
    cumulative_discount_pct = 0

    try:
        with open(source_path, 'r') as file_handle:
            for idx, raw_line in enumerate(file_handle, 1):
                try:
                    data_points = raw_line.strip().split(',')
                    if len(data_points) != 4:
                        logging.warning(f"Row {idx}: Malformed data structure, skipping.")
                        continue

                    item_label, cost_str, item_type, account_level = data_points
                    
                    original_cost = float(cost_str)
                    percent_off = get_discount(item_type, account_level)
                    
                    markdown_value = original_cost * (percent_off / 100.0)
                    net_cost = original_cost - markdown_value

                    processed_items.append({
                        'label': item_label,
                        'list_price': original_cost,
                        'rate': percent_off,
                        'savings': markdown_value,
                        'total': net_cost
                    })
                    
                    cumulative_discount_pct += percent_off

                except ValueError as err:
                    logging.error(f"Row {idx}: value interpretation error - {err}")
                    continue

        with open(dest_path, 'w') as report:
            header_rows = [
                SEPARATOR_LINE,
                "PRICING REPORT",
                SEPARATOR_LINE,
                f"{'Product Name':<30} {'Base Price':>12} {'Discount %':>12} {'Discount $':>12} {'Final Price':>12}",
                DIVIDER_LINE
            ]
            report.write('\n'.join(header_rows) + '\n')

            for item in processed_items:
                row_str = (
                    f"{item['label']:<30} "
                    f"${item['list_price']:>11.2f} "
                    f"{item['rate']:>11.1f}% "
                    f"${item['savings']:>11.2f} "
                    f"${item['total']:>11.2f}\n"
                )
                report.write(row_str)
            
            report.write(SEPARATOR_LINE + "\n")

        count = len(processed_items)
        mean_discount = (cumulative_discount_pct / count) if count > 0 else 0
        
        print("\nProcessing Complete!")
        print(f"Total products processed: {count}")
        print(f"Average discount applied: {mean_discount:.2f}%")
        print(f"Report saved to: {dest_path}")
        
        logging.info(f"Job finished. {count} items processed successfully.")

    except FileNotFoundError:
        logging.error(f"Source file missing: '{source_path}'")
        print(f"Error: Could not find {source_path}")

    except PermissionError:
        logging.error(f"Write permission denied for: '{dest_path}'")
        print(f"Error: Cannot write to {dest_path}")

    except Exception as unhandled_err:
        logging.error(f"Critical system error: {unhandled_err}")
        print(f"Error: {unhandled_err}")

if __name__ == "__main__":
    INPUT_FILENAME = 'week7/Products Pricing Manager/products.txt'
    OUTPUT_FILENAME = 'week7/Products Pricing Manager/pricing_report.txt'
    
    generate_pricing_sheet(INPUT_FILENAME, OUTPUT_FILENAME)