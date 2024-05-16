@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    print('Bot está listo y escuchando comandos!')

@client.event
async def on_message(message):
    print(f'Recibido mensaje: {message.content}')
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        command = message.content[1:].split()
        if command[0] == 'ping':
            await message.channel.send('pong!')
        elif command[0] == 'import' and len(command) == 2:
            character_id = command[1]
            url = f'https://app.demiplane.com/nexus/daggerheart/character-sheet/{character_id}'
            character_data = fetch_character_data(url)
            if character_data:
                save_character(message.author.id, character_data)
                await message.author.send(f'''```
    Personaje asignado: 

    **{character_data["name"]}**
    {character_data["class"]}, level {character_data["level"]}
```''')
            else:
                await message.channel.send('Error al importar los datos del personaje.')
        elif command[0] == 'show':
            character_data = load_character(message.author.id)
            if character_data:
                await message.channel.send(f'Tu personaje: Nombre: {character_data["name"]}, Nivel: {character_data["level"]}, Clase: {character_data["class"]}')
            else:
                await message.channel.send('No tienes un personaje asignado.')
        elif command[0] == 'agility':
            character_data = load_character(message.author.id)
            if character_data:
                mod = character_data['agility']
                result, hope, fear, _ = roll_dh(character_data['agility'])
                await message.channel.send(f'Roll 2d12+{mod}: **{result}** (Hope: {hope}, Fear: {fear})')
            else:
                await message.channel.send('No tienes un personaje asignado.')
        else:
            await message.channel.send(f'Comando `{command}` no reconocido.')