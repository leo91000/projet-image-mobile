using System;
using System.Collections.Generic;

using Xamarin.Forms;
using Xamarin.Forms.PlatformConfiguration.iOSSpecific;

namespace ImagePicker
{
    public partial class ResultsPage : ContentPage
    {
        public string sentImageUrl = "";
        private List<Result> resultList;

        public ResultsPage()
        {
            InitializeComponent();
            Title = "Results";
            On<Xamarin.Forms.PlatformConfiguration.iOS>().SetLargeTitleDisplay(LargeTitleDisplayMode.Never);
            On<Xamarin.Forms.PlatformConfiguration.iOS>().SetUseSafeArea(true);
        }

        public ResultsPage(List<Result> results, string sentPicUrl)
        {
            InitializeComponent();
            Title = "Results";
            On<Xamarin.Forms.PlatformConfiguration.iOS>().SetLargeTitleDisplay(LargeTitleDisplayMode.Never);
            On<Xamarin.Forms.PlatformConfiguration.iOS>().SetUseSafeArea(true);

            resultList = results;

            if (sentPicUrl == "")
                sentImageViewer.Source = "";
            else
                sentImageViewer.Source = ImageSource.FromUri(new Uri(sentPicUrl));
        }

        async void resultsView_ItemTapped(System.Object sender, Xamarin.Forms.ItemTappedEventArgs e)
        {
            Result r = resultList[e.ItemIndex];
            ResultZoom resultZoom = new ResultZoom(e.ItemIndex, r);
            await Navigation.PushAsync(resultZoom);
        }
    }
}
