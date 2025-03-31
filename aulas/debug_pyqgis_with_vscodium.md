# Debug de código python no QGIS usando VSCodium

Primeiro, instale o plugin **debug_vs_plugin** (Obrigado, Luiz Motta!)

No VSCodium, aperte **Ctrl+Shift+P** para abrir a barra de comandos.
- Debug: Add Configuration...
- Python Debugger
- Remote Attach
- localhost (default)
- 4678 (default)

Abra o arquivo **launch.json** e remova a parte "path_mappings", deixando apenas a seguinte configuração:
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Remote Attach",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            }
        }
    ]
}
```

Acione o plugin no QGIS no menu "Plugins -> Enable Debug for Visual Studio"  
Adicione um ponto de parado no seu código.  
Faça qualquer operação no plugin que passe pelo ponto de parada que você colocou.  

Dúvidas: https://code.visualstudio.com/docs/python/debugging

Mais informações sobre o plugin podem ser obtidas em:  
https://github.com/lmotta/debug_vs_plugin/wiki


