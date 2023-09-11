
import openai
openai.api_key = ' '

prompt_template= """ For a given set of definitions {definitions}, create {n} craetive multiple choice questions with answers to check the understanding of students of grade {grade} in the given below format
  Question:
  Options:
  Answer:
  """


def generate_definition_mcq(definitions_list, grade, n):

  prompt = prompt_template.format(definitions = definitions_list, grade = grade , n=n )
  completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0,
    messages=[
        {"role": "system", "content": 'you are a kind and helpful MCQ generator' },
      {"role": "user", "content": prompt }])
  output = completion['choices'][0]['message']['content']

  output_split = output.split('\n')
  output_strip = []
  for i in output_split:
    output_strip.append(i.strip())
  output_strip = [i for i in output_strip if i!=''] # To remove any empty strings

  questions = []
  options = []
  answers = []

  for i, string in enumerate(output_strip):
    if 'question' in string.lower():
      questions.append(string.split(':')[1].strip())
    if 'answer' in string.lower():
      answers.append(string.split(')')[1].strip())
    if 'options' in string.lower():
      options.append([output_strip[i+1][3:], output_strip[i+2][3:], output_strip[i+3][3:], output_strip[i+4][3:]])

  mcq_list = []
  for i in range(len(questions)):
    mcq_list.append({'question' : questions[i], 'options':options[i], 'answer': answers[i]})
  return mcq_list

################################


grade = '10'
n = '5'

definitions_list = ["Serendipity refers to the delightful and unexpected discovery of valuable or pleasant things by chance or accident, often when one is not actively seeking them."

,"Resilience is the ability to bounce back, adapt, and recover quickly from adversity, challenges, or setbacks. It signifies a person's or system's capacity to withstand and thrive in difficult circumstances."

,"Ephemeral describes something that is short-lived, fleeting, or transitory in nature. It is often used to refer to moments, experiences, or objects that have a brief existence."

,"Cacophony is a harsh, discordant, and unpleasant mixture of sounds or noises. It often implies a lack of harmony or a jarring combination of sounds."

,"Ubiquitous means something that is present or found everywhere, often to the extent that it seems to be all-encompassing and omnipresent."

,"Altruism is a selfless concern for the well-being and happiness of others, often demonstrated through acts of kindness, generosity, and a willingness to help without expecting anything in return."]



mcq_generated = generate_definition_mcq(definitions_list, grade, n)
mcq_generated

