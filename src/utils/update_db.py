async def update_db(bot, find_query: dict, update_data: dict, update_on: str = None,):
        try:
            data = await bot.db.guilds.find_one(find_query)
            if update_on:
                data[update_on].update(update_data)
                data.update({update_on: data[update_on]})
            else:
                data.update(update_data)
        
            await bot.db.guilds.find_one_and_replace(find_query, data)
            return True
        except Exception as e:
            bot.logger.exception(f"Error updating DB: {e}\nfind_query: {find_query}, update_data: {update_data}, update_on: {update_on}")
            return False