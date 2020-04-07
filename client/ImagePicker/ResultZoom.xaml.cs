using System;
using System.Collections.Generic;

using Xamarin.Forms;

namespace ImagePicker
{
    public partial class ResultZoom : ContentPage
    {
        public ResultZoom()
        {
            InitializeComponent();
        }

        public ResultZoom(int index, Result r)
        {
            InitializeComponent();
            resultZoomLabel.Text = "Image " + (index+1).ToString();
            imageViewer.Source = r.fullUrl;
        }
    }
}
