# Brainstorming with GPT

A Brain Diagnosis Assistant Tool

## Authors

- Waiel, Tanmay, Ashwin, Julie, Jaskirat

## Overview

Brain Chat is a dashboard that combines two main components: a chatbot and a 3D plot. The
chatbot is powered by the GPT3 model 'curie' and an input directory containing a large corpus of
text on neuroanatomy. The chatbot serves as an assistant to doctors, allowing them to input
symptoms and receive information on which parts of the brain may be affected. This feature
provides doctors with a powerful tool to diagnose and treat patients with neurological disorders.
The 3D plot is another key component of the dashboard. It allows the user to locate the parts of
the brain that are affected based on the symptoms provided by the user (doctor) and view the
cross section of the brain pertaining to the problem. This provides them with a visual
representation of the affected areas and helps them better understand the location of the lesion.
The 3D plot is interactive, allowing one to zoom in and out of different areas of the brain for a
more detailed view.
The dashboard is built using Dash Plotly in Python, a powerful web application framework for
building analytical web applications. This framework provides an intuitive interface for building
interactive dashboards and allows for seamless integration with a wide range of tools and
libraries.
The project has a wide range of potential applications in the medical field. It can be used to assist
doctors in diagnosing and treating patients with a variety of neurological disorders, including
stroke, traumatic brain injury, demyelinating diseases and neurodegenerative conditions. The
ability to locate affected areas of the brain in a visual format can also be useful in surgical
planning and rehabilitation.
Overall, the dashboard represents an innovative and powerful tool for doctors and medical
professionals. By combining the power of GPT3 with an interactive 3D plot, the dashboard
offers a comprehensive and intuitive way to localize neurological disorders. The project has the
potential to revolutionize the field of neurology and improve the lives of countless patients
around the world.

Functionality of ChatBox is shown in the figure below

<img width="415" alt="Chatbox UI" src="https://user-images.githubusercontent.com/50146522/227884693-f9ab5ba5-6866-4a11-8bf4-002b9023f3ac.png">

A small demo of this interaction is also shown below.

![chatbox](https://user-images.githubusercontent.com/50146522/227887238-19ace0a6-b88f-4a02-aff6-7caed2950dfa.gif)

In another case, we had the following conversation with our novel chatbot:

Question: A patient has Left facial droop, right arm and leg weakness. What are the possible localizations in the brain?

Answer: The possible localizations in the brain are lesions of the corticobulbar (face) and corticospinal (arm and leg) 
pathways originating in the right motor cortex. The lesion must be at or above the level of the pons, since the facial 
nerve (CN VII) nucleus is in the pons and exits the brainstem at the pontomedullary junction

It correctly pointed out the problem is in pons (region of the brain) and we got the output visualized in that region as well as seen from the animation below. That's so cool


![demo](https://user-images.githubusercontent.com/50146522/227901205-29b70bc6-8641-44cc-8e67-e706982dcb22.gif)

## Usage

- The Brain Chat dashboard can be used by doctors and medical professionals to assist them in diagnosing and treating
  patients with various neurological disorders. The chatbot component of the dashboard powered by GPT3 model 'curie' and
  the input directory containing a large corpus of text on neuroanatomy, can provide information on which parts of the
  brain may be affected based on the symptoms provided by the user. This feature can help doctors to quickly and
  accurately diagnose patients and provide appropriate treatment.

- The 3D plot component of the dashboard can be used to locate the affected areas of the brain and view the cross
  section of the brain pertaining to the problem. The interactive feature of the 3D plot allows doctors to zoom in and
  out of different areas of the brain for a more detailed view. This visual representation of the affected areas can be
  useful in surgical planning and rehabilitation.

- Overall, the Brain Chat dashboard can be a valuable tool for medical professionals in the diagnosis and treatment of
  neurological disorders. It has the potential to revolutionize the field of neurology and improve the lives of
  countless patients around the world.

<br>

*To run the app locally:*

- Navigate to the directory of the repository on the local machine.
- Ensure all the necessary packages are installed:

  `conda env create -f env.yml`
- Create a folder named `meshes` in the root directory and add the human brain object files by extracting them from
  this [link](https://gin.g-node.org/BrainGlobe/atlases/src/master/allen_human_500um_v0.1.tar.gz
  )
- Download the model named as `index.json` from
  this [link](https://drive.google.com/file/d/1QGl1k3Xb-LZNSHXXf51pPUasTjpGM4dF/view?usp=share_link) and save under
  the `dashboard_src` directory
- Edit the `credentials_template.json` file to add your open ai auth key, rename it to credentials.json.
- Verify that your project directory looks like [this]()
- Great work, you're all seet up and ready to run the app.
- Execute the following commands in a bash terminal:
  
```
cd dashboard_src
python3 app.py

```

*To propose new changes:*

- Fork the repository
- Make your changes to the code and adhere to best coding practices.
- Commit your changes (with an informative commit message).
- Push your changes to your fork - Submit a pull request.

**Places for improvement**

- Train the model on more neuro books in order to improve the model for a specialized domain.
- Improve the layout to have more professional looking Dashboard.

## License

`brainstorming-with-gpt` was created using Dash visualization by our group members. It is licensed under the terms of
the [MIT license](LICENSE).

## References

- [Brain 3D plot](https://brainglobe.info/)
- [Chat GPT models](https://openai.com/blog/introducing-chatgpt-and-whisper-apis)
- [Dataset](https://gin.g-node.org/BrainGlobe/atlases/src/master/allen_human_500um_v0.1.tar.gz)
- [PLotly](https://plotly.com/dash/)
- [BG Atlas API](https://github.com/brainglobe/bg-atlasapi)
