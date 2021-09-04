import boto3

def recreate_table(table_name):
    """Delete DynamoDB table and create it again with the same indexes"""
    # Save table indexes
    table = boto3.resource('dynamodb').Table(table_name)
    # Save KeySchema and GlobalSecondaryIndexes from the table
    original_key_schema = table.key_schema
    unfiltered_original_gsi = table.global_secondary_indexes
    
 
    gsi = []
    # Purify unfiltered_original_gsi for objects to only contain the following parameters:
    wanted_gsi_attribs = ['IndexName', 'KeySchema', 'Projection']
    # And delete all other attributes
    for index in unfiltered_original_gsi:
        obj = {}
        for key in index:
            if key in wanted_gsi_attribs:
                obj[key] = index[key]
        gsi.append(
            obj
        )

    table.delete()
        
    boto3.resource('dynamodb').create_table(
        TableName=table_name,
        KeySchema=original_key_schema,
        GlobalSecondaryIndexes=gsi,
        AttributeDefinitions=table.attribute_definitions,
        BillingMode='PAY_PER_REQUEST'
    )




#recreate_table("mytable")