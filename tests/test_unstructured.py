from unstructured.partition.auto import partition

# Parse PDF
# elements = partition("testdata/nz-itinerary-2024.pdf", strategy="hi_res")
# print("\n\n".join([str(el) for el in elements]))

# extract table from image
elements = partition("testdata/ferry-ticket.png", strategy="hi_res", 
                     infer_table_structure=True)

tables = [el for el in elements if el.category == "Table"]
print(tables[0].text)
print(tables[0].metadata.text_as_html)