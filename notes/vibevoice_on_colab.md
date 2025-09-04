# Set up VibeVoice on Google Colab

On August 26, 2025, Microsoft released [VibeVoice](https://microsoft.github.io/VibeVoice/), a Python framework and underlying model to convert text into speech. The following is a collection of its novel features as highlighted on their website:

> * VibeVoice is a novel framework designed for generating expressive, long-form, multi-speaker conversational audio, such as podcasts, from text.
> * The model can synthesize speech up to 90 minutes long with up to 4 distinct speakers, surpassing the typical 1-2 speaker limits of many prior models.

## Failed attempts
I first checked out the repository and attempted to run[inference_from_file.py](https://github.com/tejas-kale/VibeVoice/blob/main/demo/inference_from_file.py) on my M1 MacBook Air. Since the script assumes CUDA to be installed, execution failed. 

Next, using Claude Code, I adapted the script for CPU-only execution as well and applied M1-related optimisations suggested by Claude. Unfortunately, memory usage ballooned (> 16GB including swap) and each chunk of text - corresponding to about 1–2 seconds of audio - took more than 2 minutes to generate. 

I then tried further optimisations, like removing the `try-catch` blocks to prevent redundant model loads and fallback to inefficient configurations. This resolved memory bloat, possibly by making better use of the MacBook GPU, but the conversion remained slow. A short paragraph of about 100 words was still estimated to take 3 hours.

```python
APEX FusedRMSNorm not available, using native implementation
🚀 Starting VibeVoice M1-Optimized Text-to-Speech
============================================================
✓ Running on Apple Silicon: macOS-15.6.1-arm64-arm-64bit
✓ MPS device configured: mps
✓ Memory optimization configured for unified memory
📋 Configuration:
   Model: microsoft/VibeVoice-1.5b
   Text file: text_examples/noah_short.txt
   Speakers: ['Alice', 'Bob']
   Output dir: ./outputs
   CFG scale: 1.3
📖 Parsing text script...
✓ Detected multi-speaker format
✓ Found 1 dialogue segments for 1 unique speakers

📝 Parsed dialogue:
   1. Speaker 1: In February 2023, Noah posed an important question: can India industrialize? The question...
🔍 Scanning for available voice files...
✓ Found 9 voice files in /Users/tejaskale/Code/VibeVoice/demo/voices
✓ Available voice names: Alice, Anchen, Bowen, Carter, Frank, Mary, Maya, Samuel, Xinran, en-Alice_woman, en-Carter_man, en-Frank_man, en-Mary_woman_bgm, en-Maya_woman, in-Samuel_man, zh-Anchen_man_bgm, zh-Bowen_man, zh-Xinran_woman

🎭 Speaker mapping:
   Speaker 1 ('Alice') → en-Alice_woman.wav

📄 Full script preview:
   Speaker 1: In February 2023, Noah posed an important question: can India industrialize? The question has been on the minds of Indian economic policymakers since its independence in 1947. Recent attemp...

🧠 Loading VibeVoice model...
   Device: mps
   Precision: float16 (M1 optimized)
No preprocessor_config.json found at microsoft/VibeVoice-1.5b, using defaults
...
Instantiating VibeVoiceForConditionalGenerationInference model under default dtype torch.float16.
Generate config GenerationConfig {}

Instantiating Qwen2Model model under default dtype torch.float16.
Instantiating VibeVoiceAcousticTokenizerModel model under default dtype torch.float16.
Instantiating VibeVoiceSemanticTokenizerModel model under default dtype torch.float16.
Instantiating VibeVoiceDiffusionHead model under default dtype torch.float16.
Loading checkpoint shards: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3/3 [00:16<00:00,  5.60s/it]
All model checkpoint weights were used when initializing VibeVoiceForConditionalGenerationInference.

All the weights of VibeVoiceForConditionalGenerationInference were initialized from the model checkpoint at microsoft/VibeVoice-1.5b.
If your task is similar to the task the model of the checkpoint was trained on, you can already use VibeVoiceForConditionalGenerationInference for predictions without further training.
Generation config file not found, using a generation config created from the model config.
✓ Model loaded successfully
   DDPM steps: 8 (optimized for M1)

🔧 Preparing model inputs...
huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either:
	- Avoid using `tokenizers` before the fork if possible
	- Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
✓ Input tokens: 224

🎙️  Generating speech...
Generating (active: 1/1):   2%|██▋                                                                                                          | 11/448 [04:05<2:54:27, 23.95s/it]                                                                                                                                                                               
❌ Interrupted by user
```

## Switch to Colab
As recommended by the VibeVoice team, I executed their sample notebook on Google Colab with a T4 GPU. With this configuration, the same paragraph that was expected to take 3 hours on my laptop was converted to audio in approximately 1 minute. Switching to an A100 GPU increased the speed even further, which is especially beneficial for longer audio. 

However, these GPUs are not always available on the free tier. A reasonable option for consistent access is buying 50 credits for $10, valid for 3 months.

I updated the Colab notebook as follows:
1. Added support for reading files from Google Drive.
2. Added support for Markdown and EPUB files. For EPUB, only one chapter is read to keep the execution time reasonable.
3. Used GPT-5 Mini to format the text and add a "Speaker 1: " prefix where missing. VibeVoice assumes multi-speaker input, so even a single-speaker text must be marked explicitly.
4. Converted the generated `.wav` file to `.mp3` and enabled direct download.

## Formatting
VibeVoice is inconsistent with Markdown syntax. For example, italicised text such as *this* is sometimes read literally as "star this star*. It also cannot read unordered lists correctly. 

My Markdown files, often clippings of web articles via the Obsidian Web Clipper, contain metadata that must be removed. EPUB files are HTML files under the hood and also need to be converted to Markdown. 

Given these requirements, I chose to use the GPT-5 Mini model instead of complex regular expressions. GPT-5 Nano might work but is inconsistent with detailed instructions like converting unordered lists to ordered.

## Initial Output Impressions
To test the notebook, I converted Eric Barker’s article This Is How To Be An Awesome Parent: 5 Expert Insights into audio using the Frank voice. Overall, the quality was impressive.

I discovered two deficiences though:
* The voice cannot pronounce contractions like "'s" correctly. So, "let's" is pronounced at "let" and "it's" as "it".

<audio controls>
  <source src="./assets/let_pronunciation.mp3" type="audio/mpeg">
  Pronunciation of 's
</audio>

* Around the middle of the article, the narration broke down: it produced gibberish, skipped ahead, then came back to resume normally from a point further ahead. It might be due to inconsistent or illegible text that the model encountered although I couldn't spot any issues. 

Considering the following clip and see if you can follow it in the transcript below:

<audio controls>
  <source src="./assets/problems_in_the_middle.mp3" type="audio/mpeg">
  Trouble in the Middle
</audio>

[Trouble in the Middle](./assets/problems_in_the_middle.mp3)

```text
Speaker 1: What if you can’t come up with a good fantasy scenario?
Speaker 1: Then turn it into a challenge or a game. It’s not “putting on shoes”; it’s “The Great Race to See Who Can Put Shoes On Faster!” It’s not “put on your big coat”; it’s the “Winter Warrior Challenge.” You’re no longer a parent. You’re a host on the world’s least exciting game show, yelling, “WHO CAN GET TO THE CAR FASTER?!”
Speaker 1: The best part? If you pretend things are fun, often they actually end up being fun.
Speaker 1: But what if your child’s autonomy needs are extreme? Well, we can work with that too…
Speaker 1: 1.3 Offer A Choice
Speaker 1: You haven’t slept properly in months, meanwhile they wake up at dawn every day, bright-eyed, asking whether tarantulas have to go to school. So let’s discuss bedtime, a.k.a. “The Forever War.” Bedtime is the ultimate boss level of parenting.
Speaker 1: You can’t just tell them it’s time for bed. That’s for rookies. No, you give them a choice. And not a real choice, mind you, but a carefully constructed false binary:
Speaker 1: “Do you want the dinosaur pajamas or the fire truck pajamas?”
Speaker 1: Now they’re too busy pondering the relative merits of prehistoric creatures vs. emergency vehicles to even notice they’re being herded toward the inevitable.
Speaker 1: Whatever you need them to do, don’t say the standard triggering phrase. Instead, like any good huckster, assume the sale and offer a choice:
Speaker 1: “Do you want to hop to the car like a bunny or waddle like a duck?”
Speaker 1: And what if none of this works? Then we may have to resort to logic…
Speaker 1: 1.4 Try Problem-Solving
Speaker 1: You’re in the Target parking lot, and they’re losing their mind because you want to hold their hand. Of course, you can’t just say, “Hold my hand so you don’t get flattened by a Subaru,” because they’ll respond with the toddler equivalent of “You’re not the boss of me.”
Speaker 1: Here’s the four-step process to whip out:
Speaker 1: 1. Acknowledge Feelings
Speaker 1: “You don’t like your hand held in the parking lot. It makes your fingers feel squeezed.”
Speaker 1: 2. Describe The Problem
Speaker 1: Take a deep breath and say, “The problem is, I worry about cars hitting children in the parking lot.”
Speaker 1: 3. Ask For Ideas
Speaker 1: “We need some ideas so we can go back to the park and have fun. What should we do?”
Speaker 1: 4. Decide Which Ideas You Both Like
Speaker 1: At this point, you’re choosing the least ridiculous suggestion that doesn’t involve teleportation. Eventually, one idea surfaces that’s both sane and achievable: “What if I hold your sleeve?”
```

## P.S. VibeVoice Disappeared
While completing my notes, I noticed that the original VibeVoice [repository](https://github.com/microsoft/VibeVoice) was no longer available on GitHub. Reddit discussions (like [VibeVoice RIP?](https://www.reddit.com/r/LocalLLaMA/comments/1n7zk45/vibevoice_rip_what_do_you_think/)) are speculating about the reason. 

The 1.5B parameter model remains available on Huggingface and I created a [fork](https://github.com/tejas-kale/VibeVoice) of a forked repository which is now used in the Colab notebook.
