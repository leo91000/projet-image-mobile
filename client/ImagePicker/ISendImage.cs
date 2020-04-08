using System;
using System.Threading.Tasks;
using Refit;

namespace ImagePicker
{
    public interface ISendImage
    {
        [Get ("/")]
        Task<ResponseImage> GetName();

        [Multipart]
        [Post("/api/img_searches")]
        Task<ResponseImage> SendImage([AliasAs("file")] StreamPart stream);
    }
}
