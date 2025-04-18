def generate_prompt(user_input, df_columns):
    """Generate optimized prompt for code generation"""
    return f"""
    Generate Python code to analyze pandas DataFrame 'df' according to request:
    {user_input}

    STRICT RULES (NUMBERED PRIORITY):
    1. CODE STRUCTURE:
        - Return complete executable code in ```python block
        - All new variables with len(var) same lenght with len(df.shape[0]) MUST be added as new columns to existing 'df' using df['new_column'] syntax
        - Never create new DataFrames or use merge/join operations
        - Print calculation result (such as a list, Series, or array) in console
        - Define all temporary variables explicitly

    2. DATA HANDLING:
        - Use only columns from: {list(df_columns)}
        - For new data storage:
            if isinstance(result, (pd.Series, list, np.ndarray)):
                if len(result) == len(df):  # Check length match
                    df[new_col_name] = result
                else:
                    print("\\nHasil kalkulasi (ukuran {{}}):".format(len(result)))
                    print(result)
            elif isinstance(result, (int, float, str, dict, pd.DataFrame, np.ndarray)):
                print("\\nHasil skalar/metrik:")
                print(result)
            else:
                print("\\nHasil tidak tersimpan:", type(result))
        
    3. COLUMN CREATION RULES:
        a. Untuk hasil operasi matematika:
            df['hasil_kalkulasi'] = df['col1'] + df['col2']
        
        b. Untuk transformasi data:
            df['kategori_baru'] = df['col_existing'].apply(lambda x: x*2)
        
        c. Untuk agregasi grup:
            df['rata_grup'] = df.groupby('kolom_grup')['target'].transform('mean')
        
        d. Contoh khusus untuk statistik:
            # Untuk metrik seperti R2/korelasi
            corr_matrix = df.corr()
            print("\\nMatriks korelasi:")
            print(corr_matrix)
            
            # Untuk nilai skalar
            r2_score = calculate_r2()
            print("\\nR-squared:", r2_score)
        e. contoh untuk hasil prediksi
            df['Predict data'] = model.predict(X)

    4. OUTPUT HANDLING:
        Selalu cek kode untuk plot agar tidak muncul error "cannot reindex on an axis with duplicate labels"
        - Untuk hasil non-kolom (skalar/matriks/agregat):
            print("\\nHasil analisis:")
            print(result)
            
        - Untuk visualisasi WAJIB gunakan Plotly dengan contoh template:
            # JANGAN gunakan fig.show() atau renderer apapun
            Contoh untuk histogram:
            fig = px.histogram(
                df_temp,
                x=column_name,
                opacity=0.8,
                color_discrete_sequence=["#d06200"],
            )

            fig.update_traces(marker_line_color='gray', marker_line_width=0.4)

            fig.update_layout(
                template='seaborn',
                title=f"Histogram of {{column_name}}",
                xaxis_title=column_name,
                yaxis_title="Count",
                bargap=0.1
                )
            )
            
            - Berikut adalah contoh bar chart namun pastikan dulu unique value yang akan diplot kurang dari 100                   
            top_10_customers['Customer_ID'] = top_10_customers['Customer_ID'].astype(str)
            # selalu cek dulu jumlah unique value data
            if top_10_customers['Customer_ID'].unique() < 100:
                # Plot bar chart
                fig = px.bar(
                    top_10_customers,
                    x='Customer_ID',
                    y='CLV',
                    color='CLV',
                    template='plotly_dark',
                    title='Top 10 Customers by CLV',
                    category_orders={{"Customer_ID": top_10_customers['Customer_ID'].tolist()}}
                )

                # Pastikan sumbu X bertipe kategori (bukan numeric)
                fig.update_xaxes(type='category')

                fig.update_layout(
                    bargap=0.1,
                    xaxis_title='Customer ID',
                    yaxis_title='CLV',
                    hovermode='x unified'
                )
            
            Jika if top_10_customers['Customer_ID'].unique() > 100 maka buat bar chart seperti biasa, perinta ini tidak berlaku untuk chart lain seperti pie chart

            
            # Contoh scatter plot
            fig = px.scatter(
                df,
                x='col1',
                y='col2',
                color='col4',
                trendline='ols'
            )
            
            # Contoh pie chart
            # Hitung jumlah feedback
            feedback_counts = df[feedback_col].value_counts().reset_index()
            feedback_counts.columns = [feedback_col, 'count']

            # Print feedback counts
            print("\nFeedback counts:")
            print(feedback_counts)

            # Buat pie chart untuk feedback
            fig = px.pie(
                feedback_counts,
                names=feedback_col,
                values='count',
                hole=0.3,
                title='Feedback Distribution'
            )

            # Tentukan segmen terbesar dengan cara yang lebih aman
            max_segment = feedback_counts.loc[feedback_counts['count'].idxmax(), feedback_col]
            pull = [0.2 if feedback == max_segment else 0 for feedback in feedback_counts[feedback_col]]

            # Update traces untuk menarik segmen terbesar
            fig.update_traces(
                pull=pull,
                textinfo='percent+label',  # Menampilkan persentase dan label
                marker=dict(line=dict(color='#000000', width=1))  # Garis tepi untuk tiap segmen
            )

            # Update layout untuk visualisasi yang lebih baik
            fig.update_layout(
                margin=dict(t=50, b=50, l=50, r=50),
                title_x=0.5,
                legend_title_text='Kategori Feedback',  # Judul legend
                uniformtext_minsize=12,  # Ukuran teks minimal
                uniformtext_mode='hide'  # Sembunyikan teks yang tidak cukup space
            )

            # Tambahkan border ke chart
            fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
            fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)


            - Selalu gunakan border untuk chart
            - Jangan gunakan fig.show()
            - Simpan objek figure sebagai variabel


        - Untuk kolom baru:
            print(df[['kolom_baru_1', 'kolom_baru_2']].head())
        
        - Untuk operasi yang menghasilkan array ukuran berbeda:
            # Langsung print jangan simpan ke df
            conf_matrix = confusion_matrix(...)
            print("Confusion Matrix:", conf_matrix)
            
    5. ERROR PREVENTION:
        - Cek konflik nama kolom:
            if 'nama_kolom' in df.columns:
                df['nama_kolom_rev'] = ...  # tambahkan suffix jika sudah ada
        

    FINAL CHECK:
    1. Pastikan tidak ada operasi merge/join/concat
    2. Hasil dengan ukuran new_var != len(df) harus langsung di-print
    3. Skalar dan matriks tidak boleh disimpan sebagai kolom
    4. Print statement harus menunjukkan tipe hasil yang jelas
    5. Jangan menampilkan penjelasan apapun dari kode
    """
    
def prompt_chatbot(user_query, df, df1, df2):
    prompt = f"""
    Anda adalah seorang analyst. Jawab pertanyaan berikut dengan jelas 

    Pertanyaan: {user_query}
    
    jika user menanyakan data jawablah sesuai data user
    Data user: {df}, dimensinya: {df1}, tipe datanya {df2}

    Ketentuan jawaban:
    
    1. Gunakan bahasa sesuai input user
    2. Jangan sertakan contoh kode jika tidak diminta 'tampilkan kode', 'show code', 'write code'
    3. Format kode dalam blok code
    4. Jelaskan istilah teknis dengan analogi sederhana
    5. Selalu berikan tag untuk proses berpikir anda
    6. Langsung jawab pada intinya
    7. Hanya tuliskan poin-poinnya saja
    8  Jawablah sesingkat mungkin
    9. Jangan gunakan simbol yg tidak perlu di awal kalimat misal '#'
    """
    return prompt

def prompt_analyze(output, var_summaries, df, error):
    prompt = f"""
    You are a data analyst explaining Python code execution results to non-technical stakeholders.

    Execution results to analyze:
    1. Text output: {output}
    2. Generated variables: {chr(10).join(var_summaries) if var_summaries else 'No new variables created'}
    3. Errors (if any): {error if error else 'No errors'}

    Analysis format:
    A. Graphics:
    - Describe visualization type
    - Identify main patterns/trends
    - Provide business interpretation

    B. Console Output:
    - Translate numerical metrics to business context
    - Explain statistical significance
    - Highlight key decision-making metrics

    C. New Variables:
    - For new DataFrame columns: explain relationship with other columns
    - For statistical variables: explain analytical implications
    - Classify variable type (numeric/categorical/time series)

    D. Next Recommendations:
    - Suggest relevant additional analysis techniques
    - Recommend supporting visualizations
    - Identify potential data issues

    Strict rules:
    1. NEVER mention technical code details or libraries
    2. Focus on business interpretation
    3. Use everyday analogies for complex stats
    4. Prioritize actionable insights
    5. Limit to max 3 main points per category
    6. Use clear numbered bullet points

    Example structure:
    'Analysis shows:
    1. Visualization indicates... [graph interpretation]
    2. R-squared value of 0.85 suggests... [metric explanation]
    3. New "prediction" column has... [variable analysis]
    Recommendations: [specific suggestions]'

    Supporting data:
    - DataFrame dimensions: {df.shape} rows x {len(df.columns)} columns
    - Available columns: {list(df.columns)}
    - Last descriptive stats: {df.describe().to_string() if not df.empty else 'Not available'}
    """
    return prompt