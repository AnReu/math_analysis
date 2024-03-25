import comet_ml

import string
from torch import nn
import torch
from transformers import Trainer, AutoModel, TrainingArguments, AutoModelForSequenceClassification
from bert_model_layers_memory import BertForSequenceClassificationLayer

from os.path import exists

from datasets import load_from_disk
from torch.nn import LogSoftmax
import datetime
from random import randint

from sys import argv

seed = randint(0, 10000)
print('Seed:', seed)

# python3 script.py model tokenizer modeltype layer

nohead_model_path = argv[1]
tok = argv[2]
model_type = argv[3] # bert, albert, etc.
layer = argv[4]
tok_path_sanitized = tok.replace('/','_')
train_dataset = load_from_disk(f'{tok_path_sanitized}/filtered_data_train_intersect_processed')

eval_dataset = load_from_disk(f'{tok_path_sanitized}/filtered_data_eval_intersect_processed')


classes = list(string.ascii_lowercase) + ['other_class']

if model_type == 'bert':
    model = BertForSequenceClassificationLayer.from_pretrained(nohead_model_path, num_labels=len(classes), layer=layer)
elif model_type == 'albert':
    from albert_model_layers_memory import AlbertForSequenceClassificationLayer
    model = AlbertForSequenceClassificationLayer.from_pretrained(nohead_model_path, num_labels=len(classes), layer=layer)
elif model_type == 'roberta':
    from roberta_model_layers_memory import RobertaForSequenceClassificationLayer
    model = RobertaForSequenceClassificationLayer.from_pretrained(nohead_model_path, num_labels=len(classes), layer=layer)


#model_path = 'no_head_models/' + original_model_path.replace('/', '_')
#model_save_path = f'{model_path}-nothead'
#if not exists(model_path):
#	model_no_head = AutoModel.from_pretrained(original_model_path)
#	model_no_head.save_pretrained(model_save_path)


experiment_start = datetime.datetime.now().strftime("%y-%m-%d_%H:%M:%S:%f")
out_dir = f'models/{tok_path_sanitized}' +'_layer' +layer + '_'+ experiment_start + '_' + str(seed)

log_softmax = LogSoftmax(dim=1)
from datasets import load_metric
acc = load_metric("accuracy", experiment_id=str(experiment_start))
p = load_metric("precision", experiment_id=str(experiment_start))
r = load_metric("recall", experiment_id=str(experiment_start))
f1 = load_metric("f1", experiment_id=str(experiment_start))

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    logits = torch.Tensor(logits)
    labels = torch.Tensor(labels)
    print(logits.shape)
    predictions = torch.softmax(logits, dim=1)
    predictions_mask = predictions > 0.036 # 1/num_classes
    labels_mask = labels > 0.036
    
    for pred,label in zip(predictions_mask, labels_mask):
        acc.add_batch(predictions=pred, references=label)
        p.add_batch(predictions=pred, references=label)
        r.add_batch(predictions=pred, references=label)
        f1.add_batch(predictions=pred, references=label)
        
    accuracy = acc.compute()
    precision = p.compute()
    recall = r.compute()
    f1_score = f1.compute()
    return {**accuracy, **precision, **recall, **f1_score, 'loss': (-1 * torch.sum(labels * log_softmax(logits)))}


#def compute_metrics(eval_pred):
#    logits, labels = eval_pred
#    logits = torch.Tensor(logits)
#    labels = torch.Tensor(labels)
#    return {'loss': (-1 * torch.sum(labels * log_softmax(logits)))}

class CustomTrainer(Trainer):
	def compute_loss(self, model, inputs, return_outputs=False):
		labels = inputs.get("labels")
		labels[labels == 0] = -0.001
		outputs = model(**inputs)
		logits = outputs.get("logits")
	
		# bow loss from https://arxiv.org/pdf/1808.04339.pdf
		loss = -1 * torch.sum(labels * log_softmax(logits))
		return (loss, outputs) if return_outputs else loss

class F1Trainer(Trainer):
	def compute_loss(self, model, inputs, return_outputs=False):
		labels = inputs.get("labels")
		outputs = model(**inputs)
		logits = outputs.get("logits")
		predictions = torch.softmax(logits, dim=1)
		predictions_mask = predictions > 0.036 # 1/num_classes
		labels_mask = labels > 0.036
		
		pred_positives = torch.sum(predictions[predictions_mask])
		true_positives = torch.sum(predictions[labels_mask])
		all_positives = labels.shape[0]

		p = true_positives / pred_positives 
		r = true_positives / all_positives
		
		f1 = 2 * (p * r) / (p + r)
		loss = 1 - f1
		return (loss, outputs) if return_outputs else loss

for param in model.base_model.parameters():
	param.requires_grad = False

#best_hp = {'learning_rate': 9.996403781208457e-05, 'per_device_train_batch_size': 16, 'adam_beta1': 0.8130715607795982, 'adam_beta2': 0.9952387551748348, 'adam_epsilon': 6.99837179548104e-09}
best_hp = {'learning_rate': 9e-04, 'per_device_train_batch_size': 16, 'adam_beta1': 0.8130715607795982, 'adam_beta2': 0.9952387551748348, 'adam_epsilon': 6.99837179548104e-09}
#best_hp = {'learning_rate': 0.0073741789669433825, 'per_device_train_batch_size': 16, 'adam_beta1': 0.9253107033911064, 'adam_beta2': 0.8533810991045466, 'adam_epsilon': 4.4894600595512e-09}

training_args = TrainingArguments("test_trainer/trainer_"+ experiment_start + "_" + str(seed), evaluation_strategy="epoch",
				#warmup_steps=200,
				per_device_train_batch_size=16,
				per_device_eval_batch_size=16,
				learning_rate=best_hp['learning_rate'],
                                adam_beta1=best_hp['adam_beta1'],
                                adam_beta2=best_hp['adam_beta2'],
                                eval_accumulation_steps=2,
                                adam_epsilon=best_hp['adam_epsilon'],
                                #lr_scheduler_type='cosine',
				disable_tqdm=False,
				num_train_epochs=200,
                                seed=seed,
                                save_strategy='epoch',
                                load_best_model_at_end=True)
trainer = CustomTrainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=eval_dataset, compute_metrics=compute_metrics)
#trainer = CustomTrainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=eval_dataset, compute_metrics=compute_metrics)

trainer.train()

experiment = comet_ml.config.get_global_experiment()
experiment.log_parameters({
    'model_save_dir': out_dir,
    'experiment_start': experiment_start,
    'seed':seed,
    'layer': layer
})
experiment.log_parameters(training_args.to_sanitized_dict(), prefix='train_args/')

model.save_pretrained(out_dir, push_to_hub=False)
