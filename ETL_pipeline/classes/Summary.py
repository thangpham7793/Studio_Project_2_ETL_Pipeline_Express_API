from string import Template
import os
import sys


class Summary:
    summary_template = Template(
        """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="../../log_style.css" />
  <title>Document</title>
</head>
<body>
  ${summary}
</body>
</html>                                
"""
    )

    def load_success_summary(self, df, file_path):
        # NOTE: this assumes that the file is located inside ./data/dir/state/...
        state_folder = file_path.split("/")[-2]
        # in case of nested folder within a state folder (like TX/Permits/...)
        if len(state_folder) > 2:
            state_folder = file_path.split("/")[-3]

        print(file_path)

        file_name = file_path.split("/")[-1]

        for char in [" ", "#", "?", ":", ";", "%"]:
            file_name = file_name.replace(char, "_")

        log_path = f"./logs/{state_folder}/{file_name.strip()}_load_log.html"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        log = open(log_path, "w")

        try:
            # print out the first 5 values of each column
            sample_record = ""
            for col in df.columns:
                values = df[col].unique()

                # print all values if there are less than 50 unique values, or just print the first 50 unique values
                if len(values) < 50:
                    sample_values = values
                else:
                    sample_values = values[0:50]
                sample_record += f"<li style='font-weight: normal;'> <strong>{col}</strong>: {sample_values}</li>"

            summary = f"""
                      <header>
                      <h1>
                        <a name="{state_folder}">{state_folder}</a>
                      </h1>
                        <a href="../../index.html">Back to Index</a>
                        <h2>{file_path}</h2>

                        <h4>Number of Rows and Columns</h4> 
                        <p>{df.shape}</p>
                        <h4>Columns</h4> 
                      </header>
                      <main>
                        <div>
                        
                          {list(df.columns)}
                        
                        </div>
                        
                        <div>
                          <h4>Sample Record</h4>
                          <ul>
                          {sample_record}
                          </ul>
                        </div>
                        <footer>
                            <small><a href="#{state_folder}">Back to Top</a></small>
                            <small><a href="../../overview.html">Back to Index</a></small>
                        </footer>
                      </main>
                      """
        except:
            print(f"There was an error summarizing {file_path}")
            summary = (
                f"<p>There was an error summarizing {file_path}: \n{sys.exc_info()}</p>"
            )

        finally:
            log.write(self.summary_template.substitute(summary=summary))
            log.close()
