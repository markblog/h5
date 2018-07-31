import pandas as pd


def get_Custom_Asset_Class_correlation(excel_path, costom_assets = ['Active Currency', 'Australian Equity', 'Australian Shares', 'Cash',
                     'Developed Markets', 'Diversified Strategies','Emerging Markets', 'Equity', 'FX', 'Fixed Income',
                     'Global Fixed Interest', 'Grand Total', 'Hedge Funds', 'Infrastructure', 'International Equity',
                     'International shares', 'Others', 'Overlays','Private Capital', 'Property', 'TAA'], 
                     					costom_asset_attrname='Custom Asset Class',
                                       unique_mark_attrs=['Risk ID', 'Performance ID', 'Effective Date',
                                                          'Level', 'Custom Asset Class'],
                                       output_columns=['Risk ID', 'Performance ID', 'Effective Date', 'Level',
                                                       'Custom Asset Class1', 'Custom Asset Class2', 'Correlation']):
    """

    :param excel_path: str
    :param costom_assets: default is ['Active Currency', 'Australian Equity', 'Australian Shares', 'Cash',
                     'Developed Markets', 'Diversified Strategies','Emerging Markets', 'Equity', 'FX', 'Fixed Income',
                     'Global Fixed Interest', 'Grand Total', 'Hedge Funds', 'Infrastructure', 'International Equity',
                     'International shares', 'Others', 'Overlays','Private Capital', 'Property', 'TAA']
    :param costom_asset_attrname: str
    :param unique_mark_attrs: list
    :param output_columns: list
    :return: df about correlation value
    """
    data = pd.read_excel(excel_path)
    data = data[data[costom_asset_attrname].notnull()].reset_index(drop=True)

    

    result = {'Risk ID': [], 'Performance ID': [], 'Effective Date': [], 'Level': [], 'Custom Asset Class1': [],
              'Custom Asset Class2': [], 'Correlation': []}
    assets = data[costom_asset_attrname]
    for index in range(data.shape[0]):
        asset = assets[index]
        for correlation_attr in costom_assets:
            value = data[correlation_attr][index]
            if not pd.isnull(value):
                result['Risk ID'].append(data['Risk ID'][index])
                result['Performance ID'].append(data['Performance ID'][index])
                result['Effective Date'].append(data['Effective Date'][index])
                result['Level'].append(data['Level'][index])
                result['Custom Asset Class1'].append(asset)
                result['Custom Asset Class2'].append(correlation_attr)
                result['Correlation'].append(value)
    df = pd.DataFrame.from_dict(result)
    return df[output_columns]  # reorganize df column's order


if __name__ == '__main__':
    ll = ['Active Currency', 'Australian Equity', 'Australian Shares', 'Cash',
          'Developed Markets', 'Diversified Strategies', 'Emerging Markets', 'Equity', 'FX', 'Fixed Income',
          'Global Fixed Interest', 'Grand Total', 'Hedge Funds', 'Infrastructure', 'International Equity',
          'International shares', 'Others', 'Overlays', 'Private Capital', 'Property', 'TAA']
    res = get_Custom_Asset_Class_correlation('Singular Entity Analysis Data Source Automated v8.xlsx', ll)
    print(res)
