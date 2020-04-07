using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Net.Http;
using Xamarin.Forms;
using Refit;
using Plugin.Media.Abstractions;
using Plugin.Media;

namespace ImagePicker
{
    [DesignTimeVisible(false)]
    public partial class MainPage : TabbedPage
    {
        private string serverUrl = "https://ns3017873.ip-149-202-86.eu";
        private string postUrl = "/api/img_searches/";
        private string dateFormat = "yyyy-MM-dd_hh-mm-ss";
        private Dictionary<string, List<Result>> queryList;
        private List<List<Result>> queries;

        public MainPage()
        {
            InitializeComponent();
            Title = "FashionistApp";

            queryList = new Dictionary<string, List<Result>>();
            imageViewer.Source = new Image().Source;
            queries = new List<List<Result>>();
        }

        void Toast(string message)
        {
            DependencyService.Get<IMessage>().ShortAlert(message);
        }

        async void uploadPicture(Stream stream, HttpClient apiClient, ISendImage imageServerApi)
        {
            // POST request

            string queryId = "";
            ResponseImage response = new ResponseImage();

            try
            {
                await DisplayAlert("Sending a picture", "Send the selected picture?", "OK", "Cancel");

                debugger.Text = "Sending...";
                activityIndicator.IsVisible = true;
                activityIndicator.IsRunning = true;
                imageUploadButton.IsEnabled = false;
                imageUploadButton.Text = "Sending...";

                string filename = DateTime.Now.ToString(dateFormat) + ".jpg";
                response = await imageServerApi.SendImage(new StreamPart(stream, filename));
                queryId = response.id.ToString();
            }
            catch (Refit.ApiException apiException)
            {
                debugger.Text = "Header (Request):\n" + apiClient.DefaultRequestHeaders.ToString() + "\nHeader (Response):\n" + apiException.Headers.ToString() + "\nBody (Response):\n" + apiException.Message.ToString();
            }
            finally
            {
                debugger.Text = "Header (Request):\n" + apiClient.DefaultRequestHeaders.ToString() + "\nHeader (Response):\n" + response.id + "/" + response.name + "/" + response.results + "/";
            }

            // GET request

            response = new ResponseImage();
            apiClient.BaseAddress = new Uri(serverUrl + postUrl + queryId);

            try
            {
                imageUploadButton.Text = "Retrieving response...";
                response = await imageServerApi.GetName();
                photoTakenViewer.Source = new Image { Source = ImageSource.FromUri(new Uri("http://" + response.url)) }.Source;
                debugger2.Text = response.url;
            }
            catch (Refit.ApiException)
            {
                await DisplayAlert("Error", "Server unreachable.", "OK");
            }

            activityIndicator.IsRunning = false;
            activityIndicator.IsVisible = false;
            imageUploadButton.IsEnabled = true;
            imageUploadButton.Text = "Select another picture";

            try
            {
                int i = 1;

                List<Result> latestQuery = response.results;
                queries.Add(latestQuery);

                foreach (Result r in latestQuery)
                {
                    r.fullUrl = "http://" + r.url;
                    r.similarityPercentage = (Math.Round(r.score, 3) * 100).ToString() + " %";
                    r.title = "Image " + i;
                    r.subtitle = r.url.Split('/').ElementAt(1);
                    i++;
                }

                queryList.Add(queryId, latestQuery);

                // Refresh the queryView list
                queryView.ItemsSource = null;
                queryView.ItemsSource = queryList.Keys;

                ContentPage resultsPage = new ResultsPage(latestQuery, "http://" + response.url);

                Label queryNumberLabel = (Label)resultsPage.FindByName("queryNumberLabel");
                queryNumberLabel.Text = "Query #" + queryId;

                ListView resultsView = (ListView)resultsPage.FindByName("resultsView");
                resultsView.ItemsSource = latestQuery;

                Image sentImageViewer = (Image)resultsPage.FindByName("sentImageViewer");
                sentImageViewer.Source = "http://" + response.url;

                await Navigation.PushAsync(resultsPage);
            }
            catch (System.NullReferenceException)
            {
                await DisplayAlert("Error", "Server unreachable.", "OK");
            }
        }

        async void queryView_ItemTapped(System.Object sender, Xamarin.Forms.ItemTappedEventArgs e)
        {
            if(queryView.ItemsSource != null)
            {
                ResultsPage resultsFromQueryListPage = new ResultsPage(queries.ElementAt(e.ItemIndex), "");

                ListView resultsView = (ListView)resultsFromQueryListPage.FindByName("resultsView");
                resultsView.ItemsSource = queryList.Values.ElementAt(e.ItemIndex);

                Label queryIdLabel = (Label)resultsFromQueryListPage.FindByName("queryNumberLabel");
                queryIdLabel.Text = queryList.Keys.ElementAt(e.ItemIndex);

                await Navigation.PushAsync(resultsFromQueryListPage);
            }
        }

        async void imageUploadButton_ClickedAsync(System.Object sender, System.EventArgs e)
        {
            string action = await DisplayActionSheet("Select a picture", "Cancel", null, "From Gallery", "Take a picture");

            var apiClient = new HttpClient();
            apiClient.BaseAddress = new Uri(serverUrl);
            var imageServerApi = RestService.For<ISendImage>(apiClient);

            switch (action)
            {
                case "From Gallery":
                    Stream streamFromGallery = await DependencyService.Get<IPhotoPickerService>().GetImageStreamAsync();
                    if(streamFromGallery != null)
                        uploadPicture(streamFromGallery, apiClient, imageServerApi);

                    break;

                case "Take a picture":
                    await CrossMedia.Current.Initialize();

                    if (!CrossMedia.Current.IsCameraAvailable || !CrossMedia.Current.IsTakePhotoSupported)
                    {
                        await DisplayAlert("No Camera", "No camera available.", "OK");
                        return;
                    } else
                    {
                        var file = await CrossMedia.Current.TakePhotoAsync(new StoreCameraMediaOptions
                        {
                            Directory = "Sample",
                            Name = "test.jpg"
                        });

                        if (file == null)
                            return;

                        await DisplayAlert("File Location", file.Path, "OK");
                        uploadPicture(file.GetStream(), apiClient, imageServerApi);

                        /*
                         * photoTakenViewer.Source = ImageSource.FromStream(() =>
                        {
                            var stream = file.GetStream();
                            return stream;
                        });
                         */

                    }

                    break;

                case "Cancel":
                    //
                    break;
            }
        }
    }
}
