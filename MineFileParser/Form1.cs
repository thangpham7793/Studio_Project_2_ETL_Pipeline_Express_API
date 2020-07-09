using System;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;

namespace MineFileParser
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            this.AllowDrop = true;
        }

        private void processCSVFile(string filePath)
        {
            StreamReader file = new StreamReader(filePath);
            string line = "";

            List<string[]> splitObjects = new List<string[]>();

            int index = 0;
            while((line = file.ReadLine()) != null)
            {
                if(line.Contains("Active") || line.Contains("active") || index == 0)
                {
                    if(line.Contains("Surface") || line.Contains("surface") || line.Contains("Facility") || line.Contains("facility") || index == 0)
                    {
                        string[] splitLine = line.Split('|');
                        string[] compressedLine = {splitLine[1], splitLine[3], splitLine[4], splitLine[5], splitLine[7], splitLine[9], splitLine[10], splitLine[13],
                            splitLine[22], splitLine[26], splitLine[30], splitLine[32], splitLine[43], splitLine[44], splitLine[57], splitLine[58] };
                        splitObjects.Add(compressedLine);
                    }
                    
                }
                index++;
            }

            Console.WriteLine(splitObjects.Count.ToString());
            index = 0;
            foreach(string[] sArr in splitObjects)
            {
                //First item - Contains labels
                if (index == 0)
                {
                    int index2 = 0;
                    foreach (string s in sArr)
                    {
                        dataGridView1.Columns.Add(s, s);
                        index2++;
                    }
                }
                else
                {
                    dataGridView1.Rows.Add(sArr);
                }
                index++;
            }
        }

        private void Form1_DragEnter(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop)) e.Effect = DragDropEffects.Copy;
        }

        private void Form1_DragDrop(object sender, DragEventArgs e)
        {
            string[] csvFile= (string[])e.Data.GetData(DataFormats.FileDrop);
            processCSVFile(csvFile[0]);
        }
    }
}
