# Kubes

## Purposes
- `kubes ls` to list pods(default), ns, secrets etc.
- `kubes cx` to list all namespaces or switch one.
- `kubes log` to show logs by a number of the tail or streaming with `--follow`.
- `kubes cp` to copy a file or directory between pod and local.
- `kubes run` to interact with a pod.
- The program is using __stdout__ and __stderr__ which means it's able to support the next level deployment scripting.

## Installation
```bash
pip install kubes
```

## Instruction
### - `kubes ls <subjects>`
This command render the form with color, and track `STATUS` column. If the status is not in [`Running`, `Active`], it will be marked by red.
![kube_ls_demo_img](https://github.com/Ron-Chang/kubes/blob/develop/img/demo.png)



## Usage
```
kubes.py [-h] {ls,cx,log,cp,run} ...

optional arguments:
  -h, --help          show this help message and exit

subcommands:
  List Subjects

  {ls,cx,log,cp,run}
    ls                List Subject [default value: pods]
    cx                List namespaces or switch the context to one of them
    log               Show logs
    cp                Download file or directory
    run               Execute pod with command default: bash
```

## Update Logs
|#|      date|version|
|-|----------|-------|
|6|2021/05/17| v1.1.0|
|5|2021/05/17| v1.0.1|
|4|2021/05/16| v1.0.0|
|3|2021/05/15| v0.1.0|
|2|2021/05/13| v0.0.6|
|1|2021/05/13| v0.0.1|

## 1.1.0
- Use full pod name to check pods instead of name without hash

## 1.0.1
- Removed detect command timeout in 10 seconds to avoid copy files overtime

## 1.0.0
- First release version
- Update README.md

## 0.1.0
- Restructure arguments by group

## 0.0.6
- Add streaming arguments and add tail numbers for pods logs
- Dye the pods status if it shows not Running

If you like my work, please consider buying me a coffee or [PayPal](https://paypal.me/RonDevStudio?locale.x=zh_TW)
Thanks for your support! Cheers! 🎉
<a href="https://www.buymeacoffee.com/ronchang" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" align="right"></a>
