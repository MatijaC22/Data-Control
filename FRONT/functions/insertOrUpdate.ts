// myScript.ts

export function deleteImage(allImagesNames:string[], allImages:string[], uploadedImage:string[], i:number){
    allImagesNames.splice(i,1)
    allImages.splice(i,1)
    uploadedImage.splice(i,1);
    return {allImagesNames:allImagesNames, allImages:allImages, uploadedImage:uploadedImage}
};
export const handleImageUpload = (event, component) => {
    const file = event.target.files[0];
  
    if (file) {
      const reader = new FileReader();
  
      reader.onload = () => {
        // Save the image data or perform other actions
        component.allImages.push(event.target.files[0]);
        component.uploadedImages.push(reader.result);
      };
  
      reader.readAsDataURL(file);
    }
  };
  export const submitData = async function (component) {
    if (component.Description && component.JobId && component.UserId) {
      component.login_in_submission = true;
      component.login_show_alert = true;
  
      let userData = {
        id: component.Id,
        description: component.Description,
        user_id: component.UserId,
        job_id: component.JobId,
      };
  
      if (component.Id) {
        await component.updateUser(userData);
  
        if (component.ImageUrl === '' && component.selectedImages) {
          await component.uploadImage(component.id, component.selectedImages);
        }
      } else {
        await component.insertUser(userData);
  
        if (component.ImageUrl === '' && component.selectedImages) {
          await component.uploadImage(component.id, component.selectedImages);
        }
      }
  
      setTimeout(() => {
        component.$emit('closeWindow', userData);
        if (!component.Id) {
          // window.location.reload();
        }
      }, 1000);
    }
  };

  