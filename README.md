# FLO_CLTV_and_Segmentation
CLTV Prediction with BG-NBD and Gamma-Gamma and customer segmentation (RFM)

# TASKS

# CLTV
  ## TASK 1: Preparing the Data
              # 1. Read the data flo_data_20K.csv. Make a copy of the dataframe.
              #2. Define the outlier_thresholds and replace_with_thresholds functions needed to suppress outliers.
              # Note: When calculating cltv, frequency values must be integers. Therefore, round the lower and upper limits with round().
              # 3. Set the variables "order_num_total_ever_online","order_num_total_ever_offline","customer_value_total_ever_offline","customer_value_total_ever_online"
              # suppress outliers if any.
              # 4. Omnichannel means that customers shop from both online and offline platforms. Total for each customer
              # create new variables for number of purchases and spend.
              # 5. Examine the variable types. Change the type of variables that express date to date.

  ## TASK 2: Creating CLTV Data Structure
              # 1. Take 2 days after the date of the last purchase in the data set as the date of analysis.
              # Create a new cltv dataframe with the values 2.customer_id, recency_cltv_weekly, T_weekly, frequency and monetary_cltv_avg.
              # Monetary value will be expressed as average value per purchase, recency and tenure values will be expressed in weekly terms.


  ## TASK 3: BG/NBD, Establishing Gamma-Gamma Models, Calculating CLTV
              # 1. Fit the BG/NBD model.
                   # a. Estimate expected purchases from customers in 3 months and add exp_sales_3_month to cltv dataframe.
                   # b. Estimate expected purchases from customers in 6 months and add exp_sales_6_month to cltv dataframe.
              # 2. Fit the Gamma-Gamma model. Estimate the average value of the customers and add it to the cltv dataframe as exp_average_value.
              # 3. Calculate 6 months CLTV and add it to the dataframe with the name cltv.
                   # a. Standardize the cltv values you calculated and create the scaled_cltv variable.
                   # b. Observe the 20 people with the highest Cltv value.

  ## TASK 4: Creating Segments by CLTV
              # 1. Divide all your customers into 4 groups (segments) according to the 6-month standardized CLTV and add the group names to the dataset. Add it to the dataframe with the name cltv_segment.
              # 2. Make short 6-month action suggestions to the management for 2 groups you will choose from among 4 groups.

  ## TASK 5: Functionalize the whole process.

# RFM

## TASK 1: Data Understanding and Preparation
            # 1. Read the flo_data_20K.csv data.
            #2. In the dataset
                      # a. top 10 observations,
                      # b. variable names,
                      # c. descriptive statistics,
                      # D. null value,
                      # e. Variable types, review.
            # 3. Omnichannel means that customers shop from both online and offline platforms. Total for each customer
            # create new variables for number of purchases and spend.
            # 4. Examine the variable types. Change the type of variables that express date to date.
            # 5. Look at the breakdown of the number of customers, average number of products purchased, and average spend in shopping channels.
            # 6. Rank the top 10 customers with the most revenue.
            # 7. Rank the top 10 customers with the most orders.
            # 8. Functionalize the data provisioning process.

## TASK 2: Calculating RFM Metrics

## TASK 3: Calculating RF and RFM Scores

## TASK 4: Defining RF Scores as Segments

## TASK 5: Time for action!
            # 1. Examine the recency, frequency and monetary averages of the segments.
            # 2. With the help of RFM analysis, find the customers in the relevant profile for 2 cases and save the customer IDs to the csv.
                    # a. FLO includes a new women's shoe brand. The product prices of the brand it includes are above the general customer preferences. Therefore, the brand
                    It is desired to contact the customers in the profile that will be interested in # promotion and product sales. From their loyal customers(champions,loyal_customers),
                    # People who shop from the women category with an average of 250 TL or more are the customers who will be contacted privately. Id numbers of these customers to csv file
                    # save as new_brand_target_customer_id.cvs.
                    # b. Up to 40% discount is planned for Men's and Children's products. Good past customer but long-standing customer interested in categories related to this sale
                    # customers who should not be lost who do not shop, those who are asleep and new customers are specifically targeted. Enter the ids of the customers in the appropriate profile into the csv file discount_target_customer_ids.csv
                    Save it as #.


## TASK 6: Functionalize the whole process.
