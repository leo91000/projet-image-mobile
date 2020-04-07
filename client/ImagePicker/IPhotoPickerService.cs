using System.IO;
using System.Threading.Tasks;

namespace ImagePicker
{
    public interface IPhotoPickerService
    {
        Task<Stream> GetImageStreamAsync();
    }
}