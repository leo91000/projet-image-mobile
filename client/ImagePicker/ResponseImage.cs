using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace ImagePicker
{
    public class ResponseImage
    {
        public int id { get; set; }
        public string name { get; set; }
        public string url { get; set; }
        public List<Result> results { get; set; }

        public string GetName()
        {
            return "";
        }

        public string SendImage(byte[] imgBytes)
        {
            string queryId = "";

            // queryId = response

            return queryId;
        }
    }

    public class Result
    {
        public string url { get; set; }
        public string fullUrl { get; set; }
        public double score { get; set; }
        public string similarityPercentage { get; set; }
        public string title { get; set; }
        public string subtitle { get; set; }
    }
}
