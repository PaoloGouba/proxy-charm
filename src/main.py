from data_extractor import DataExtractor

def main():
    data_extractor = DataExtractor()

    # Altri dettagli del tuo script di scraping...
    
    data_extractor.add_data("Site1", site1_data)
    data_extractor.add_data("Site2", site2_data)

    data_extractor.to_xml()
    data_extractor.to_json()
    data_extractor.to_csv()

if __name__ == "__main__":
    main()
