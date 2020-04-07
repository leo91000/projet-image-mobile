using System;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace ImagePicker
{
    public partial class App : Application
    {
        public App()
        {
            InitializeComponent();

            //MainPage = new MainPage();

            if (Device.RuntimePlatform == Device.iOS)
                MainPage = new NavigationPage(new MainPage());
            else
                MainPage = new MainPage();
        }

        protected override void OnStart()
        {
        }

        protected override void OnSleep()
        {
        }

        protected override void OnResume()
        {
        }
    }
}
